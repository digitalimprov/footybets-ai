# 🚀 GitHub + Cloud Build Integration Setup Guide

## ✅ What's Already Done

- ✅ Cloud Storage bucket created: `gs://footybets-ai-static`
- ✅ Brownlow content uploaded to Cloud Storage
- ✅ Cloud Build API enabled
- ✅ `cloudbuild.yaml` configuration file created

## 🔗 Step 1: Connect GitHub Repository

### Option A: Through Google Cloud Console (Recommended)

1. **Go to Cloud Build Triggers**:
   - Visit: https://console.cloud.google.com/cloud-build/triggers
   - Select project: `footybets-ai`

2. **Connect Repository**:
   - Click "Connect Repository"
   - Choose "GitHub (Cloud Build GitHub App)"
   - Click "Install Google Cloud Build GitHub App"
   - Select your repository: `digitalimprov/footybets-ai`
   - Click "Connect"

### Option B: Through GitHub

1. **Install Cloud Build GitHub App**:
   - Go to: https://github.com/apps/google-cloud-build
   - Click "Install"
   - Select your repository: `digitalimprov/footybets-ai`

## 🔧 Step 2: Create Build Trigger

1. **In Cloud Build Console**:
   - Click "Create Trigger"
   - Name: `footybets-deploy-trigger`
   - Description: `Deploy FootyBets.ai on push to main branch`

2. **Repository Settings**:
   - Repository: `digitalimprov/footybets-ai`
   - Branch: `^main$` (regex pattern)

3. **Build Configuration**:
   - Build configuration: `cloudbuild.yaml`
   - Location: Repository

4. **Advanced Settings**:
   - Service account: `Default compute service account`
   - Region: `us-central1`

5. **Click "Create"**

## 🔐 Step 3: Set Environment Variables

1. **Create Secret for Gemini API Key**:
   ```bash
   echo "your-actual-gemini-api-key" | gcloud secrets create gemini-api-key --data-file=-
   ```

2. **Grant Cloud Build Access**:
   ```bash
   PROJECT_NUMBER=$(gcloud projects describe footybets-ai --format="value(projectNumber)")
   gcloud secrets add-iam-policy-binding gemini-api-key \
       --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
       --role="roles/secretmanager.secretAccessor"
   ```

3. **Update cloudbuild.yaml**:
   - Replace `${_GEMINI_API_KEY}` with the secret reference
   - The trigger will automatically use the secret

## 🚀 Step 4: Test the Integration

1. **Make a small change**:
   ```bash
   # Edit any file
   echo "# Test update" >> README.md
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```

3. **Monitor deployment**:
   - Go to: https://console.cloud.google.com/cloud-build/builds
   - Watch the build progress
   - Check your deployed services after 5-10 minutes

## 📋 Your Daily Workflow

Once set up, your workflow becomes:

1. **Edit in Cursor** ✅
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Update prediction algorithm"
   git push origin main
   ```
3. **Automatic deployment** (5-10 minutes) ✅

## 🔗 Your Live URLs

- **Frontend**: https://footybets-frontend-818397187963.us-central1.run.app
- **Backend**: https://footybets-backend-818397187963.us-central1.run.app
- **API Docs**: https://footybets-backend-818397187963.us-central1.run.app/docs

## 🆘 Troubleshooting

### If builds fail:
1. Check Cloud Build logs: https://console.cloud.google.com/cloud-build/builds
2. Verify environment variables are set correctly
3. Check that `cloudbuild.yaml` is in the root directory

### If GitHub connection fails:
1. Reinstall the Cloud Build GitHub App
2. Check repository permissions
3. Verify the repository URL is correct

## 🎉 Success!

Once this is set up, you'll have:
- ✅ **Automatic deployments** on every push to main
- ✅ **Version control** for all changes
- ✅ **Easy rollbacks** if needed
- ✅ **Professional CI/CD pipeline**

Your FootyBets.ai will be automatically updated every time you push code to GitHub! 🚀 