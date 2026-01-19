# Collagen Segmentation and CFOD Features

This repository contains code and resources for the segmentation of collagen and the extraction of Collagen Fibre Orientation Disorder (CFOD) features.

## Getting Started

### Overview

Collagen segmentation plays a crucial role in the analysis of histopathological images, providing valuable insights into tissue structure and disorder. CFOD features are extracted to quantify collagen fiber orientation, providing a key biomarker for various biomedical applications.

### Documentation

To gain a deeper understanding of the Collagen Segmentation process and CFOD features, please refer to the detailed guide provided in the link below:
I still have few doubts like this: [**Issue**](https://github.com/GriffinLab/BIFs/issues/1)

[**A Beginner's Guide to Collagen Fibre Detection**](https://github.com/Emory-Empathathetic-AI-for-Health-Inst/CFOD/blob/main/A%20beginner's%20guide%20to%20Collagen%20Fibre%20detection%20%26.pdf)

This document will walk you through the key concepts, methodologies, and workflows involved in collagen fiber segmentation and feature extraction.

### Usage
You need to provide, image patches and their corresponding stromal masks. It will save a .json file for CFOD features for all the window sizes, which later you can use for calculating features like mean, max, mode etc

## Important Info
This is the exact replica of parameters used by Haojia Li

