---
title: Multi-Nuclear MRI
date: 2022-10-18T17:04:07+01:00
draft: false
layout: research_area
header_img: 'img/research/na_bkg.jpg'

sections:
  - heading: "Image2Flow"
    text: "Computational fluid dynamics (CFD) can be used for non-invasive evaluation of hemodynamics. However, its routine use is limited by labor-intensive manual segmentation, CFD mesh creation, and time-consuming simulation. This study aims to train a deep learning model to both generate patient-specific volume-meshes of the pulmonary artery from 3D cardiac MRI data and directly estimate CFD flow fields. This proof-of-concept study used 135 3D cardiac MRIs from both a public and private dataset. The pulmonary arteries in the MRIs were manually segmented and converted into volume-meshes. CFD simulations were performed on ground truth meshes and interpolated onto point-point correspondent meshes to create the ground truth dataset. The dataset was split 110/10/15 for training, validation, and testing. Image2Flow, a hybrid image and graph convolutional neural network, was trained to transform a pulmonary artery template to patient-specific anatomy and CFD values, taking a specific inlet velocity as an additional input. Image2Flow was evaluated in terms of segmentation, and the accuracy of predicted CFD was assessed using node-wise comparisons. In addition, the ability of Image2Flow to respond to increasing inlet velocities was also evaluated. Image2Flow achieved excellent segmentation accuracy with a median Dice score of 0.91 (IQR: 0.86–0.92). The median node-wise normalized absolute error for pressure and velocity magnitude was 11.75% (IQR: 9.60–15.30%) and 9.90% (IQR: 8.47–11.90), respectively. "
    images:
      - "img/research_areas/simulation/image2flow.png"
      

  - heading: "Implementation"
    text: "The simulation was implemented using a custom framework designed for scalability."
    images:
      - "img/research_areas/simulation/image2flow.png"

  - heading: "Results"
    text: "Results showed strong correlation with empirical observations under controlled conditions."
---
