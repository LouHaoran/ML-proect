--record of commandline of libsvn run on Windows
--For convenience I put the files in one folder.. all in ./libsvm-3.23/Windows
--To replicate the results, make sure you are in this path..


--------------------------------------------------------------------------

Microsoft Windows [Version 10.0.17763.437]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\lou>cd C:\Users\lou\Downloads\libsvm-3.23\windows

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-train.exe -t 0 training.new Train\Kernel0
....*....*
optimization finished, #iter = 579
nu = 0.017662
obj = -0.627017, rho = 1.172955
nSV = 40, nBSV = 0
Total nSV = 40

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-train.exe -t 1 training.new Train\Kernel1
.*.*
optimization finished, #iter = 162
nu = 0.022567
obj = -0.801149, rho = 0.404372
nSV = 57, nBSV = 0
Total nSV = 57

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-train.exe -t 2 training.new Train\Kernel2
.*
optimization finished, #iter = 99
nu = 0.801753
obj = -30.091940, rho = -0.076980
nSV = 71, nBSV = 22
Total nSV = 71

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-train.exe -t 3 training.new Train\Kernel3
*
optimization finished, #iter = 37
nu = 0.957746
obj = -65.367107, rho = -0.492870
nSV = 68, nBSV = 68
Total nSV = 68

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-predict.exe validation.new Train\Kernel0 Test\test0
Accuracy = 85.7143% (30/35) (classification)

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-predict.exe validation.new Train\Kernel1 Test\test1
Accuracy = 74.2857% (26/35) (classification)

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-predict.exe validation.new Train\Kernel2 Test\test2
Accuracy = 77.1429% (27/35) (classification)

C:\Users\lou\Downloads\libsvm-3.23\windows>svm-predict.exe validation.new Train\Kernel3 Test\test3
Accuracy = 45.7143% (16/35) (classification)

C:\Users\lou\Downloads\libsvm-3.23\windows>