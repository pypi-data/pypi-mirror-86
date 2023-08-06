$WriteProps = @{
    'BucketName' = 'm3base1020x'                              # S3 Bucket Name
    'Key'        = 'gitlab-demo-only/hello-ct.zip'            # Key used to identify the S3 Object
    'File'       = 'codetrace-pse.zip'                        # Local File to upload
    'Region'     = 'eu-west-1'                                # AWS Region
    'AccessKey'  = 'AKIA5P3QHMQAILPJ4DHY'                     # AWS Account Access Key
    'SecretKey'  = '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' # AWS Account Secret Key
}
Write-Host "Zipping packages..." 
$path = split-path (Get-Item .).FullName -Parent
Compress-Archive -Path "$path\dist\" -DestinationPath codetrace-pse.zip
Write-Host "Uploading to S3..."
Write-S3Object @WriteProps
Write-Host "Upload success..."