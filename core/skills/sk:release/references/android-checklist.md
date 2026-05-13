# Android / Play Store Readiness Checklist

Walk through every section below. For each item, check the relevant file, report status, and fix or guide as needed.

---

## 1. Google Play Developer Account

- [ ] Developer account exists at https://play.google.com/console
- [ ] One-time $25 registration fee paid
- [ ] Developer profile completed (name, email, website, phone)
- [ ] If using Google Play App Signing (recommended), enrollment is done

**First-time guidance**: Walk the user through creating an account if they don't have one.

---

## 2. App Identity

### Package Name / Application ID
- Check `app.json` > `expo.android.package` (Expo)
- Check `android/app/build.gradle` > `applicationId` (RN bare / native)
- Check `pubspec.yaml` or `android/app/build.gradle` (Flutter)
- Must be reverse-domain format: `com.company.appname`
- Must be unique on Play Store — cannot be changed after first publish
- No uppercase letters, no hyphens, only dots and lowercase alphanumeric

### Version Code & Version Name
- `versionCode` must be an integer, must increment with every upload
- `versionName` is the user-facing version string (e.g., "1.0.0")
- For Expo: check `app.json` > `expo.android.versionCode` and `expo.version`
- For bare RN/native: check `android/app/build.gradle` > `defaultConfig`
- WARN if versionCode is 1 and this is an update (should be incremented)

---

## 3. App Signing

### Expo (EAS Build)
- Check if `eas.json` exists with a `production` profile
- Verify `"credentialsSource": "remote"` (recommended) or local keystore configured
- EAS manages signing automatically — confirm `eas credentials` has been run

### React Native (bare) / Native Android
- Check for `*.keystore` or `*.jks` file
- Check `android/app/build.gradle` for `signingConfigs.release`
- Check `android/gradle.properties` for keystore password references
- WARN if passwords are hardcoded (should use env vars or `gradle.properties` excluded from git)
- Verify `.gitignore` includes `*.keystore`, `*.jks`

### Flutter
- Check `android/app/build.gradle` for `signingConfigs`
- Check for `key.properties` file
- Verify `key.properties` is in `.gitignore`

### Play App Signing (all frameworks)
- Recommend enrollment in Google Play App Signing
- If using upload key + signing key model, verify upload key is configured

---

## 4. AndroidManifest.xml

Location varies by framework:
- Expo: auto-generated, check `app.json` > `expo.android.permissions`
- RN bare: `android/app/src/main/AndroidManifest.xml`
- Flutter: `android/app/src/main/AndroidManifest.xml`
- Native: `app/src/main/AndroidManifest.xml`

### Permissions Audit
- List all declared permissions
- WARN on dangerous permissions that need justification:
  - `READ_CONTACTS`, `ACCESS_FINE_LOCATION`, `CAMERA`, `RECORD_AUDIO`, `READ_PHONE_STATE`
  - `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE` (deprecated in API 33+)
  - `QUERY_ALL_PACKAGES` (needs declaration form)
- FAIL if permissions are declared but not actually used in code
- For Expo: check `app.json` > `expo.android.permissions` array

### Internet Permission
- Must have `android.permission.INTERNET` (usually default)

### Intent Filters
- Check for deep link / app link intent filters
- If app uses deep links, verify `autoVerify="true"` and `assetlinks.json` is hosted

---

## 5. Target SDK & API Levels

### Current Google Play Requirements (2024+)
- `targetSdkVersion` must be **34** (Android 14) or higher for new apps
- `minSdkVersion` — recommend **24** (Android 7.0) or higher for broad compatibility
- `compileSdkVersion` should match or exceed `targetSdkVersion`

### Where to check
- Expo: `app.json` > `expo.android.targetSdkVersion` (or defaults from Expo SDK version)
- RN bare / native: `android/app/build.gradle` > `defaultConfig`
- Flutter: `android/app/build.gradle` > `defaultConfig`

### FAIL conditions
- `targetSdkVersion` < 34
- `compileSdkVersion` < `targetSdkVersion`

---

## 6. App Bundle (AAB)

- Google Play requires **Android App Bundle (.aab)** format (not APK) for new apps
- Verify build configuration produces AAB:
  - Expo/EAS: default for production builds
  - RN bare: `./gradlew bundleRelease`
  - Flutter: `flutter build appbundle`
  - Native: Gradle `bundleRelease` task

### ProGuard / R8
- Check if code shrinking is enabled for release builds
- `android/app/build.gradle` > `buildTypes.release.minifyEnabled`
- If enabled, verify ProGuard rules don't strip needed classes
- For RN: check `proguard-rules.pro` includes React Native rules

### 64-bit Support
- All native libraries must include 64-bit (`arm64-v8a`) builds
- Check `android/app/build.gradle` > `ndk.abiFilters`
- Should include at minimum: `armeabi-v7a`, `arm64-v8a`

---

## 7. App Icons & Assets

### Launcher Icon
- Must provide adaptive icon (foreground + background layers)
- Sizes: 512x512 for Play Store listing, various mipmap sizes for device
- Expo: check `app.json` > `expo.android.adaptiveIcon`
  - `foregroundImage`: must exist and be at least 1024x1024
  - `backgroundColor`: should be set
- RN bare / native: check `android/app/src/main/res/mipmap-*` directories
- Flutter: check `android/app/src/main/res/mipmap-*`

### FAIL conditions
- No icon configured
- Icon is placeholder/default
- Foreground image smaller than 512x512

---

## 8. Splash Screen

- Expo: check `app.json` > `expo.splash` and `expo.android.splash`
- RN bare: check for splash screen library configuration
- Should not show default/placeholder splash

---

## 9. Privacy & Data Safety

### Privacy Policy
- **REQUIRED** for all apps on Google Play
- Must be a publicly accessible URL
- Expo: check `app.json` > `expo.android.privacyPolicyUrl` or metadata
- Must cover: what data is collected, how it's used, third-party sharing

### Data Safety Form
- Must be completed in Play Console before publishing
- Covers: data collection, sharing, security practices, data deletion
- Guide user through the form based on what the app actually does:
  - Does the app use analytics? (Firebase, Amplitude, etc.)
  - Does the app collect personal info? (email, name, etc.)
  - Does the app use location?
  - Does the app use advertising IDs?
  - Does the app allow user-generated content?

### MANUAL CHECK: Provide a checklist of questions to determine data safety answers

---

## 10. Content Rating

- Must complete content rating questionnaire in Play Console (IARC)
- App will be rated based on content (violence, language, etc.)
- MANUAL CHECK: Remind user to complete this in Play Console

---

## 11. Store Listing

All required for Play Store:

- [ ] **App name** (max 30 characters)
- [ ] **Short description** (max 80 characters)
- [ ] **Full description** (max 4000 characters)
- [ ] **App icon** (512x512 PNG, 32-bit, no alpha)
- [ ] **Feature graphic** (1024x500 PNG or JPEG)
- [ ] **Screenshots** — minimum 2, recommended 8
  - Phone: 16:9 or 9:16, min 320px, max 3840px per side
  - 7-inch tablet: optional but recommended
  - 10-inch tablet: optional but recommended
- [ ] **App category** selected
- [ ] **Contact email** provided
- [ ] **Privacy policy URL** provided

### MANUAL CHECK: Guide user on preparing these assets

---

## 12. Testing Track

Recommend using testing tracks before production:

1. **Internal testing** — up to 100 testers, instant publish
2. **Closed testing** — invite-only, good for beta
3. **Open testing** — anyone can join
4. **Production** — public release

For first-time apps, suggest starting with Internal Testing.

---

## 13. Build & Submit Commands

### Expo (EAS)
```bash
# First time setup
npx eas-cli login
npx eas-cli build:configure

# Build for Android
npx eas-cli build --platform android --profile production

# Submit to Play Store
npx eas-cli submit --platform android --profile production
```
Note: EAS Submit requires a Google Play Service Account key (`sa_key.json`). Guide user through creating one in Google Cloud Console if not present.

### React Native (bare)
```bash
cd android && ./gradlew bundleRelease
# Output: android/app/build/outputs/bundle/release/app-release.aab
# Upload manually via Play Console or use `fastlane supply`
```

### Flutter
```bash
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
# Upload manually via Play Console or use `fastlane supply`
```

### Native Android
```bash
./gradlew bundleRelease
# Upload via Play Console
```

---

## 14. Common Rejection Reasons

Check for these before submitting:

1. **Crashes on launch** — test on a real device or emulator before submitting
2. **Missing privacy policy** — required for all apps
3. **Misleading metadata** — app description must match actual functionality
4. **Broken functionality** — all advertised features must work
5. **Intellectual property** — no trademarked names/logos without permission
6. **Background location** — requires extra justification form if used
7. **All Files Access** — `MANAGE_EXTERNAL_STORAGE` needs approval form
8. **Accessibility services** — if using AccessibilityService API, needs declaration
9. **SMS/Call Log permissions** — restricted, needs declaration form
10. **Photos/Videos permission** — use granular media permissions on API 33+
