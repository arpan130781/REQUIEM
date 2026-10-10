import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import os
import argparse

# ---------------------------------------------------------
# REQUIEM: Conv-TasNet Speech Enhancement Architecture
# Target: INT8 Edge Inference on Kendryte K210
# ---------------------------------------------------------

class ConvTasNet(nn.Module):
    def __init__(self, N=256, L=20, B=256, H=512, P=3, X=8, R=4):
        """
        Compact Conv-TasNet Configuration for low-resource deployment.
        N: Number of filters in autoencoder
        L: Length of filters
        B: Number of channels in bottleneck
        H: Number of channels in convolutional blocks
        P: Kernel size in convolutional blocks
        X: Number of convolutional blocks in each repeat
        R: Number of repeats
        """
        super(ConvTasNet, self).__init__()
        # Encoder
        self.encoder = nn.Conv1d(1, N, L, stride=L//2, bias=False)
        
        # Separation Configuration (TCN)
        self.tcn = nn.Sequential(
            nn.LayerNorm(N),
            nn.Conv1d(N, B, 1)
        )
        # Simplified Temporal Convolutional Network for K210 footprint
        self.repeats = nn.ModuleList([
            self._build_repeats(B, H, P, X) for _ in range(R)
        ])
        
        self.mask_conv = nn.Conv1d(B, N, 1)
        # Decoder
        self.decoder = nn.ConvTranspose1d(N, 1, L, stride=L//2, bias=False)

    def _build_repeats(self, B, H, P, X):
        blocks = []
        for x in range(X):
            dilation = 2**x
            padding = (P - 1) * dilation // 2
            blocks.append(nn.Sequential(
                nn.Conv1d(B, H, 1),
                nn.PReLU(),
                nn.GroupNorm(1, H),
                nn.Conv1d(H, H, P, dilation=dilation, padding=padding, groups=H),
                nn.PReLU(),
                nn.GroupNorm(1, H),
                nn.Conv1d(H, B, 1)
            ))
        return nn.Sequential(*blocks)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)
            
        # 1. Encoder
        enc_out = self.encoder(x)
        enc_relu = torch.relu(enc_out)
        
        # 2. Separation (Mask estimation)
        tcn_out = self.tcn(enc_relu)
        for repeat in self.repeats:
            tcn_out = repeat(tcn_out) + tcn_out
        
        mask = torch.sigmoid(self.mask_conv(tcn_out))
        
        # 3. Apply Mask and Decode
        masked_enc = enc_relu * mask
        out = self.decoder(masked_enc)
        return out.squeeze(1)

# ---------------------------------------------------------
# SI-SNR Loss Function
# ---------------------------------------------------------
def si_snr_loss(estimated, original, eps=1e-8):
    """ Scale-Invariant Signal-to-Noise Ratio (SI-SNR) """
    estimated = estimated - torch.mean(estimated, dim=-1, keepdim=True)
    original = original - torch.mean(original, dim=-1, keepdim=True)
    
    target_energy = torch.sum(original**2, dim=-1, keepdim=True) + eps
    proj = torch.sum(estimated * original, dim=-1, keepdim=True) * original / target_energy
    noise = estimated - proj
    
    snr = 10 * torch.log10(torch.sum(proj**2, dim=-1) / (torch.sum(noise**2, dim=-1) + eps) + eps)
    return -torch.mean(snr)  # Negative because we minimize loss

# ---------------------------------------------------------
# Dummy Dataset for Defence Noise Pipeline
# ---------------------------------------------------------
class DefenceNoiseDataset(Dataset):
    def __init__(self, data_dir, snr_range=(-5, 15)):
        self.data_dir = data_dir
        self.snr_range = snr_range
        print(f"Initialized dataset with defence noise categories: Gunfire, Artillery, Vehicles, Helicopters, Jets, Footsteps, Radio Chatter.")

    def __len__(self):
        return 1000  # Placeholder size

    def __getitem__(self, idx):
        # In a real scenario, this would load clean speech, pick a random defence noise,
        # mix them at a random SNR, and apply augmentations (reverb, clipping).
        # Returning dummy 1-second 16kHz tensors.
        clean = torch.randn(16000)
        noisy = clean + 0.5 * torch.randn(16000) 
        return noisy, clean

# ---------------------------------------------------------
# Training Pipeline
# ---------------------------------------------------------
def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on {device}...")
    
    model = ConvTasNet().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-5)
    
    train_dataset = DefenceNoiseDataset(args.data_dir)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    
    model.train()
    for epoch in range(args.epochs):
        epoch_loss = 0.0
        for batch_idx, (noisy, clean) in enumerate(train_loader):
            noisy, clean = noisy.to(device), clean.to(device)
            
            optimizer.zero_grad()
            enhanced = model(noisy)
            loss = si_snr_loss(enhanced, clean)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
            optimizer.step()
            
            epoch_loss += loss.item()
            
        print(f"Epoch {epoch+1}/{args.epochs} - SI-SNR Loss: {epoch_loss/len(train_loader):.4f}")
        
    torch.save(model.state_dict(), "requiem_tasnet_latest.pth")
    print("Model saved to requiem_tasnet_latest.pth")
    
    # Export to ONNX for the Kendryte NNCase compiler
    dummy_input = torch.randn(1, 16000, device=device)
    torch.onnx.export(model, dummy_input, "requiem_tasnet.onnx", opset_version=11)
    print("Exported ONNX model for K210 deployment.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data", help="Path to defence dataset")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    args = parser.parse_args()
    train(args)
