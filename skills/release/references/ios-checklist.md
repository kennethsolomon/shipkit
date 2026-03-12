# iOS / App Store Readiness Checklist

Walk through every section below. For each item, check the relevant file, report status, and fix or guide as needed.

---

## 1. Apple Developer Account

- [ ] Enrolled in Apple Developer Program at https://developer.apple.com
- [ ] $99/year membership is active
- [ ] Team / individual account type chosen
- [ ] Agreements in App Store Connect are all accepted (check for updated agreements — this blocks submissions)

**First-time guidance**: Walk the user through enrollment. Note: can take 24-48 hours for approval.

---

## 2. App Identity

### Bundle Identifier
- Must be reverse-domain format: `com.company.appname`
- Must be unique on App Store — cannot be changed after first publish
- Expo: check `app.json` > `expo.ios.bundleIdentifier`
- RN bare: check `ios/<AppName>.xcodeproj/project.pbxproj` > `PRODUCT_BUNDLE_IDENTIFIER`
- Flutter: check `ios/Runner.xcodeproj/project.pbxproj` or `ios/Runner/Info.plist`
- Native: check Xcode project settings > General > Bundle Identifier

### Version & Build Number
- `CFBundleShortVersionString` — user-facing version (e.g., "1.0.0")
- `CFBundleVersion` — build number, must increment with every upload
- Expo: check `app.json` > `expo.version` and `expo.ios.buildNumber`
- RN bare / native: check `Info.plist` or Xcode project settings
- Flutter: check `pubspec.yaml` > `version` (format: "1.0.0+1" where +1 is build number)

---

## 3. Code Signing

### Expo (EAS Build)
- Check if `eas.json` exists with a `production` profile
- Verify `"credentialsSource": "remote"` (recommended — EAS manages certs automatically)
- Or check for local provisioning profile and distribution certificate
- Confirm `eas credentials` has been configured

### React Native (bare) / Native iOS
- Check for valid Apple Distribution Certificate
- Check for App Store provisioning profile (not Ad Hoc or Development)
- Verify Xcode project settings:
  - `CODE_SIGN_IDENTITY` = "Apple Distribution" (or "iPhone Distribution")
  - `PROVISIONING_PROFILE_SPECIFIER` is set
  - `CODE_SIGN_STYLE` = "Manual" (recommended for CI) or "Automatic"
- If using Automatic Signing, verify Apple ID is configured in Xcode

### Flutter
- Same as native iOS — check `ios/Runner.xcodeproj` signing settings
- Verify `ios/ExportOptions.plist` if building from CLI

### WARN conditions
- Development provisioning profile used instead of Distribution
- Ad Hoc profile used instead of App Store profile
- Certificate expiring within 30 days

---

## 4. Info.plist

Location varies by framework:
- Expo: auto-generated from `app.json`, check `expo.ios.infoPlist` for overrides
- RN bare: `ios/<AppName>/Info.plist`
- Flutter: `ios/Runner/Info.plist`
- Native: `<Target>/Info.plist`

### Required Permission Descriptions (Usage Descriptions)
Apple REJECTS apps that request permissions without explaining why. Check for these keys and verify descriptions are user-friendly and specific:

| Permission | Info.plist Key | Example Description |
|---|---|---|
| Camera | `NSCameraUsageDescription` | "Take profile photos" |
| Photo Library | `NSPhotoLibraryUsageDescription` | "Select images to upload" |
| Location (in use) | `NSLocationWhenInUseUsageDescription` | "Show nearby restaurants" |
| Location (always) | `NSLocationAlwaysUsageDescription` | "Track your run in background" |
| Microphone | `NSMicrophoneUsageDescription` | "Record voice messages" |
| Contacts | `NSContactsUsageDescription` | "Find friends on the app" |
| Calendar | `NSCalendarsUsageDescription` | "Add events to your calendar" |
| Face ID | `NSFaceIDUsageDescription` | "Unlock the app with Face ID" |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` | "Connect to nearby devices" |
| Tracking | `NSUserTrackingUsageDescription` | "Deliver personalized ads" |

**FAIL conditions:**
- Permission key exists but description is empty or generic ("This app needs access")
- Permission is requested in code but key is missing from Info.plist
- Permission key exists but the app doesn't actually use that permission (remove it)

### App Transport Security (ATS)
- Check for `NSAppTransportSecurity` in Info.plist
- `NSAllowsArbitraryLoads = YES` will trigger review scrutiny — needs justification
- WARN if arbitrary loads are enabled; recommend using exceptions for specific domains instead
- For Expo: check `app.json` > `expo.ios.infoPlist.NSAppTransportSecurity`

### Other Required Keys
- `UIRequiredDeviceCapabilities` — verify only capabilities the app truly needs
- `UISupportedInterfaceOrientations` — verify matches app design
- `UILaunchStoryboardName` — must be present (usually "SplashScreen" or "LaunchScreen")

---

## 5. Privacy Manifest (Required since Spring 2024)

Apple now requires a **Privacy Manifest** (`PrivacyInfo.xcprivacy`) for:
- Apps that use certain APIs (Required Reason APIs)
- Apps that include SDKs on Apple's list of SDKs requiring privacy manifests

### Required Reason APIs to check for:
- `NSUserDefaults` — reason: "CA92.1" (app functionality)
- `fileTimestamp` APIs — file modification dates
- `systemUptime` / `mach_absolute_time` — system boot time
- `diskSpace` APIs — available disk space
- `activeKeyboards` — user's keyboard list

### Where to check
- Expo: SDK 50+ handles this automatically for built-in modules. Check if third-party libraries need entries.
- RN bare / native: check `ios/PrivacyInfo.xcprivacy` exists
- Flutter: check `ios/Runner/PrivacyInfo.xcprivacy`

### FAIL conditions
- No `PrivacyInfo.xcprivacy` and app uses Required Reason APIs
- Privacy manifest doesn't declare all Required Reason APIs used

### How to fix
Create or update `PrivacyInfo.xcprivacy` with the correct `NSPrivacyAccessedAPITypes` entries. Provide the exact XML for the user's detected API usage.

---

## 6. App Icons

### Required
- 1024x1024 App Store icon (no alpha channel, no rounded corners — Apple applies them)
- Expo: check `app.json` > `expo.icon` and `expo.ios.icon`
- RN bare / native: check `ios/<AppName>/Images.xcassets/AppIcon.appiconset`
- Flutter: check `ios/Runner/Assets.xcassets/AppIcon.appiconset`

### FAIL conditions
- No icon configured
- Icon includes alpha/transparency (App Store rejects this)
- Icon is a placeholder
- Icon contains text that's too small to read
- `Contents.json` in the asset catalog is incomplete

---

## 7. Launch Screen / Splash Screen

- Must have a launch screen (Apple rejects apps without one)
- Expo: check `app.json` > `expo.splash` and `expo.ios.splash`
- RN bare: check `ios/<AppName>/LaunchScreen.storyboard` or `LaunchScreen.xib`
- Flutter: check `ios/Runner/Base.lproj/LaunchScreen.storyboard`
- Must not be a plain blank white/black screen (Apple may reject)

---

## 8. Deployment Target

### Minimum iOS Version
- Check `IPHONEOS_DEPLOYMENT_TARGET` in Xcode project
- Expo: determined by Expo SDK version (SDK 51+ requires iOS 15.1+)
- Recommend: iOS 16.0+ for new apps (covers ~95% of active devices)
- WARN if targeting below iOS 15

### Supported Architectures
- Must support `arm64` (all modern iPhones)
- Should NOT include `i386` or `x86_64` only (simulator-only archs)
- Check `ARCHS` and `VALID_ARCHS` in build settings

---

## 9. Privacy & Data Collection

### Privacy Policy
- **REQUIRED** for all apps on the App Store
- Must be a publicly accessible URL
- Expo: often set in `app.json` or in App Store Connect
- Must cover: what data is collected, how it's used, third-party sharing, data retention, deletion

### App Privacy Details (Nutrition Labels)
- Must be completed in App Store Connect
- Covers categories: Contact Info, Health & Fitness, Financial Info, Location, etc.
- For each data type: collected? linked to identity? used for tracking?
- Guide user through based on actual app behavior:
  - Analytics SDKs (Firebase, Amplitude, Mixpanel)
  - Authentication data (email, name, phone)
  - Location services
  - Device identifiers
  - Crash reporting (Sentry, Bugsnag)

### App Tracking Transparency (ATT)
- If the app tracks users across apps/websites, must implement ATT framework
- Must show the ATT prompt before tracking
- Check for `NSUserTrackingUsageDescription` in Info.plist
- If app doesn't track users, verify no tracking SDKs are included

---

## 10. App Store Connect Setup

### Create App Record
- Log in to https://appstoreconnect.apple.com
- Create new app with matching Bundle ID
- Select primary language and category

### Required Store Listing Assets
- [ ] **App name** (max 30 characters)
- [ ] **Subtitle** (max 30 characters, optional but recommended)
- [ ] **Description** (max 4000 characters)
- [ ] **Keywords** (max 100 characters, comma-separated)
- [ ] **Support URL**
- [ ] **Marketing URL** (optional)
- [ ] **Privacy Policy URL** (required)
- [ ] **App icon** (1024x1024, uploaded during build or manually)

### Screenshots (REQUIRED)
Must provide for at least these device sizes:
- **6.7" iPhone** (1290x2796 or 2796x1290) — iPhone 15 Pro Max
- **6.5" iPhone** (1284x2778 or 2778x1284) — iPhone 14 Plus (can reuse 6.7")
- **5.5" iPhone** (1242x2208 or 2208x1242) — iPhone 8 Plus
- **iPad Pro 12.9" 6th gen** (2048x2732) — if app supports iPad
- **iPad Pro 12.9" 2nd gen** (2048x2732) — if app supports iPad

Minimum 1 screenshot per size, maximum 10. Recommended: 4-8 screenshots.

### MANUAL CHECK: Guide user on taking/creating screenshots

---

## 11. App Review Guidelines — Common Rejections

Check the app against these common rejection reasons:

### 1. Crashes & Bugs
- App must not crash on launch
- All advertised features must work
- Test on a real device before submitting

### 2. Minimum Functionality
- Apple rejects "simple websites wrapped in an app" (WebView-only apps)
- App must provide value beyond what a website offers
- If the app is primarily a WebView, it needs substantial native features

### 3. In-App Purchase Requirements
- **Digital goods/services MUST use Apple's In-App Purchase** (Apple takes 15-30%)
- Physical goods/services CAN use external payment (Stripe, etc.)
- Reader apps (Netflix, Spotify) can link to external sign-up since 2022
- FAIL if the app sells digital content without IAP

### 4. Login Requirements
- If app requires login, must support "Sign in with Apple" (if any third-party social login is offered)
- Guest access or demo mode recommended for review
- Provide test credentials in App Store Connect review notes

### 5. Privacy
- Must have privacy policy
- Must declare all data collection accurately
- Must not access unnecessary device capabilities

### 6. Metadata
- Screenshots must reflect actual app experience
- Description must match functionality
- App name must not include pricing info or "free"

### 7. Age Rating
- Must be accurate — Apple verifies this
- If app has user-generated content, must include: reporting, blocking, content moderation

### 8. Background Modes
- Only declare background modes (`UIBackgroundModes`) that the app actually uses
- FAIL if unused background modes are declared (common reason for rejection)
- Check Info.plist for: `audio`, `location`, `voip`, `fetch`, `remote-notification`, `processing`

---

## 12. Build & Submit Commands

### Expo (EAS)
```bash
# First time setup
npx eas-cli login
npx eas-cli build:configure

# Build for iOS
npx eas-cli build --platform ios --profile production

# Submit to App Store
npx eas-cli submit --platform ios --profile production
```
Note: EAS Submit requires an App Store Connect API key. Guide user through creating one in App Store Connect > Users and Access > Keys if not present.

### React Native (bare)
```bash
# Archive in Xcode: Product > Archive
# Or from CLI:
xcodebuild -workspace ios/App.xcworkspace -scheme App -configuration Release archive -archivePath build/App.xcarchive
xcodebuild -exportArchive -archivePath build/App.xcarchive -exportOptionsPlist ios/ExportOptions.plist -exportPath build/

# Upload via Xcode Organizer, Transporter app, or `xcrun altool`
```

### Flutter
```bash
flutter build ipa --release
# Output: build/ios/ipa/*.ipa
# Upload via Xcode, Transporter, or `xcrun altool`
```

### Native iOS
```
# Archive via Xcode: Product > Archive
# Upload via Xcode Organizer or Transporter
```

---

## 13. TestFlight (Recommended Before Production)

- Upload build to App Store Connect
- It will be available in TestFlight within minutes (internal) or after beta review (external)
- Internal testers: up to 100, no review needed
- External testers: up to 10,000, requires beta review (usually <24 hours)
- Recommend at least internal TestFlight testing before production submission

---

## 14. Review Preparation

Before submitting for review, prepare:

- [ ] **Demo account** — if app requires login, provide test credentials in review notes
- [ ] **Review notes** — explain any non-obvious functionality, required hardware, etc.
- [ ] **Contact info** — phone number and email for the review team
- [ ] **App-specific features** — if using restricted entitlements (HealthKit, HomeKit, etc.), provide documentation
- [ ] **Export compliance** — declare if app uses encryption (most apps do via HTTPS — answer "Yes" and mark as exempt under standard exemptions)
