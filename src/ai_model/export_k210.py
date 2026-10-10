"""
REQUIEM: K210 NNCase Compilation Script
Converts the PyTorch-exported ONNX model to a K210 compatible '.kmodel'
Applies INT8 Post-Training Quantization (PTQ) using calibration data.
"""

import os
import subprocess

def compile_kmodel():
    onnx_path = "requiem_tasnet.onnx"
    kmodel_path = "requiem_tasnet_int8.kmodel"
    calibration_dataset = "./data/calibration/" # Sample audio for INT8 calibration
    
    if not os.path.exists(onnx_path):
        print(f"Error: {onnx_path} not found. Train the model first.")
        return

    print("Starting NNCase compiler for K210 (INT8 Quantization)...")
    
    # NNCase v0.2 command line arguments for KPU target
    command = [
        "ncc", "compile",
        onnx_path,
        kmodel_path,
        "-i", "onnx",
        "-t", "k210",
        "--dataset", calibration_dataset,
        "--dataset-format", "raw",
        "--inference-type", "uint8",
        "--calibrate-method", "kl_divergence"
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Success! Model compiled to {kmodel_path}")
        print("You can now flash this to the K210 Flash memory using kflash.py")
    except Exception as e:
        print("NNCase compilation failed. Make sure nncase is installed in PATH.")

if __name__ == "__main__":
    compile_kmodel()
