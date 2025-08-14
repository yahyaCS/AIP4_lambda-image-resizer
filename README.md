# AWS Lambda – Image Resizer & End-of-Day Cleanup

## 📌 Overview
This project contains **two AWS Lambda functions** integrated with Amazon S3 and EventBridge:

1. **Image Resizer** (Deployed via AWS Serverless Application Repository)  
   - Automatically resizes images uploaded to an S3 bucket.
   - Triggered by S3 events.

2. **End-of-Day Cleanup**  
   - Deletes or cleans up files from the S3 bucket at a scheduled time.
   - Triggered by an AWS EventBridge cron schedule.

---

## 🛠 Project Architecture
    
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │   User Upload   │───▶│  S3 Event Trigger│───▶│ Image Resizer   │
    │  Image to S3    │    │ (originals/ only)│    │ Lambda Function │
    └─────────────────┘    └──────────────────┘    └─────────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────────┐
                                                   │ Resized Image Saved │
                                                   │ to S3 /resized/     │
                                                   └─────────────────────┘
    
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │  EventBridge    │───▶│   Daily Cron     │───▶│ EOD Cleanup     │
    │ (CloudWatch)    │    │  22:10 UTC       │    │ Lambda Function │
    └─────────────────┘    └──────────────────┘    └─────────────────┘
                                                            │
                                                            ▼
                                                   ┌────────────────────┐
                                                   │ originals/ &       │
                                                   │ resized/ cleared   │
                                                   └────────────────────┘
---

## Project Structure
    
      | Path                               | Description                    |
      | ---------------------------------- | ------------------------------ |
      | `image-resizer/`                   | SAR-deployed Lambda function   |
      | `image-resizer/lambda_function.py` | Code for image resizing        |
      | `eod-cleanup/`                     | Custom cleanup Lambda function |
      | `eod-cleanup/cleanup_lambda.py`    | Code for scheduled cleanup     |
      | `README.md`                        | Project documentation          |



## 📂 Function Details

### 1️⃣ Image Resizer
- **Trigger:** S3 `ObjectCreated` event.
- **Purpose:** Automatically resize uploaded images and store them in a destination bucket or prefix.
- **Technologies:** AWS Lambda, boto3, Pillow (PIL).
- **Key Environment Variables:**
  ```
  | Variable        | Description               | Default        |
  | --------------- | ------------------------- | -------------- |
  | `DEST_BUCKET`   | Destination bucket name   | Same as source |
  | `DEST_PREFIX`   | Prefix for resized images | `resized/`     |
  | `TARGET_WIDTH`  | Target image width        | `800`          |
  | `TARGET_HEIGHT` | Target image height       | `600`          |

---

### 2️⃣ End-of-Day Cleanup
- **Trigger:** AWS EventBridge Scheduled Rule.
- **Purpose:** Remove or clean up specific objects from S3.
- **Technologies:** AWS Lambda, boto3.
- **Schedule:** Runs **daily at 3:10 AM PKT** (22:10 UTC).
- **Cron Expression:**
  ```
  cron(10 22 * * ? *)

---

## 🚀 Deployment

### **1. Deploy Image Resizer (SAR)**
1. Go to **AWS Lambda → Create function → Browse serverless app repository**.
2. Search for `"image-resizer"` and deploy.
3. Update the environment variables as needed.
4. Connect to your S3 bucket’s `ObjectCreated` trigger.

---

### **2. Deploy EOD Cleanup Lambda**
1. Create a new Lambda function (`Python 3.13` runtime).
2. Upload `cleanup_lambda.py` as the handler code.
3. Set the handler name to:
   ```bash
   cleanup_lambda.lambda_handler
4. Add IAM permissions for S3 read/write.
5. Create an **EventBridge Rule**:
- Name: `bucket-eod-cleanup`
- Schedule expression:
  ```
  cron(10 22 * * ? *)
  ```
- Target: The cleanup Lambda function.

---

## 📜 Testing

### **Image Resizer**
1. Upload an image to the `originals/` folder in your S3 bucket.
2. Check the `resized/` folder for the resized version.

### **EOD Cleanup**
- **Manual Test:** Invoke the Lambda function manually from the AWS console.
- **Scheduled Test:** Wait for the next 3:10 AM PKT schedule to trigger automatically.

---

## 🛡 IAM Permissions

Both functions require:
  ```json
      {
      "Version": "2012-10-17",
      "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject"
         ],
         "Resource": "arn:aws:s3:::<your-bucket-name>/*"
       }
      ]
      }
```

## 📊 Monitoring

- Track Lambda execution logs for both upload and cleanup functions using AWS CloudWatch

- Monitor EventBridge schedules for cleanup jobs.

## 🖼 Verification Images

### Originals Images Folder

<img width="1437" height="578" alt="image" src="https://github.com/user-attachments/assets/9271e69c-f328-474e-9c5c-2a173cd524b2" />


### Resized Images Folder

<img width="1134" height="459" alt="image" src="https://github.com/user-attachments/assets/ba20e8f3-f29b-46b0-9dbb-e5425c221119" />


### Log Stream after uploading - Lambda `image resizer` function

<img width="1430" height="486" alt="image" src="https://github.com/user-attachments/assets/157acf7e-a98c-4407-a089-38cbc50de0a5" />

### S3 after EOD cleanup with cron job

<img width="1139" height="493" alt="image" src="https://github.com/user-attachments/assets/3740aa23-8df2-428f-98a5-37d9ae9edd23" />

### Amazon EventBridge Schedule

<img width="1142" height="595" alt="image" src="https://github.com/user-attachments/assets/6f1d9ae5-fdf6-4b42-8ea4-f2d7b6f76917" />

### Log Stream after cleanup - Lambda `buket-eod-cleanup` function + AWS Eventbridge EOD cleanup with cron job

<img width="1426" height="451" alt="image" src="https://github.com/user-attachments/assets/57d45ca2-beee-423c-950a-a87b092f15b7" />

## ⚠️ Important: Remove Cron Job After Verification

After verifying that the EOD cleanup Lambda function works as expected

**Action Steps:**
1. Open the **Amazon EventBridge** console.
2. Locate the scheduled rule for the cleanup function.
3. **Disable** or **delete** the rule immediately after verification.

---

✅ This project successfully implements an automated image processing and cleanup workflow on AWS, ensuring efficiency, scalability, and cost-effectiveness.




