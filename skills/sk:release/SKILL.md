---
name: sk:release
description: "Automate releases: bump version, update CHANGELOG, create git tag, push to GitHub. Supports --android and --ios flags to run a full App Store / Play Store readiness audit before release — checks configs, permissions, signing, icons, store listing requirements, and guides you step-by-step through fixes. Use this whenever someone wants to release, publish, deploy, or submit an app to the App Store, Play Store, Google Play, or Apple App Store."
disable-model-invocation: true
argument-hint: "[android|ios]"
---

# Release Automation Skill

Automate the release process with optional mobile store submission review.

## Modes

| Invocation | What happens |
|---|---|
| `/sk:release` | Git release only: version bump, CHANGELOG, tag, push |
| `/sk:release --android` | Git release + Play Store readiness audit |
| `/sk:release --ios` | Git release + App Store readiness audit |
| `/sk:release --android --ios` | Git release + both store audits |

## Step 1: Detect Flags

Parse the user's invocation for `--android` and/or `--ios` flags.

- If **no flags**: run the standard git release flow (Step 2 only)
- If **flags present**: run Step 2 (git release), then Step 3 (store audit for each flag)

## Step 2: Standard Git Release

Run the existing release script (`release.sh`) which handles:

1. Auto-detect project info (name, version, GitHub URL)
2. Prompt for new version number (semver)
3. Update CHANGELOG.md ([Unreleased] -> [Version])
4. Update version in CLAUDE.md
5. Create git commit + annotated tag
6. Push tag to GitHub

If no flags were passed, stop here.

## Step 3: Mobile Store Audit

When `--android` or `--ios` flags are present, run the store readiness audit AFTER the git release completes.

### 3a. Auto-Detect Framework

Detect the mobile framework by checking for these files (in order):

| Check | Framework |
|---|---|
| `app.json` or `app.config.js` or `app.config.ts` with `"expo"` key | **Expo** |
| `react-native.config.js` or `node_modules/react-native` | **React Native (bare)** |
| `pubspec.yaml` with `flutter` dependency | **Flutter** |
| `build.gradle` + `AndroidManifest.xml` (no RN/Flutter markers) | **Native Android (Kotlin/Java)** |
| `*.xcodeproj` or `*.xcworkspace` (no RN/Flutter markers) | **Native iOS (Swift/ObjC)** |
| `.NET MAUI` or `maui` in csproj | **.NET MAUI** |
| `capacitor.config.ts` or `capacitor.config.json` | **Capacitor/Ionic** |

Report the detected framework to the user. If detection fails, ask them.

### 3b. Detect Store History

Check if the app has been previously submitted:

- **Android**: Look for `android/app/sk:release/` builds, `google-services.json`, existing `sa_key.json` (service account), or `android/app/build.gradle` with a `versionCode` > 1
- **iOS**: Look for existing provisioning profiles in `ios/`, `ExportOptions.plist`, or `app.json` with an existing `bundleIdentifier` that follows reverse-domain convention with a real domain

Report whether this appears to be a **first-time submission** or an **update to an existing app**.

### 3c. Run the Audit

Based on the detected flags, read and execute the corresponding checklist:

- `--android`: Read `references/android-checklist.md` and walk through every section
- `--ios`: Read `references/ios-checklist.md` and walk through every section

For each checklist item:

1. **Check** — Read the relevant config file and evaluate the requirement
2. **Report** — Tell the user the status (PASS / FAIL / WARN / MANUAL CHECK NEEDED)
3. **Fix** — If it's a config issue you can fix, propose the fix and apply it with user approval
4. **Guide** — If it requires manual action (screenshots, store listing, etc.), give clear step-by-step instructions

### 3d. Summary Report

After completing the audit, present a summary:

```
## Store Readiness Report

### Android (Play Store)     <-- if --android
- [x] App signing configured
- [x] Version code incremented
- [ ] Privacy policy URL missing  <-- actionable items
- [ ] Store listing screenshots needed

### iOS (App Store)           <-- if --ios
- [x] Bundle ID configured
- [x] Info.plist permissions
- [ ] App Transport Security exception needs justification

### Next Steps
1. Fix the items marked above
2. [Framework-specific build command]
3. [Framework-specific submit command]
```

## Important Behaviors

- Always check files before suggesting changes — never assume config values
- For first-time submissions, include account setup guidance (Developer Console / App Store Connect)
- For Expo projects, prefer EAS Build/Submit commands over manual native builds
- Be explicit about costs ($25 Google Play one-time fee, $99/year Apple Developer Program)
- When fixing config files, show the diff and get approval before applying
- If both `--android` and `--ios` are passed, run Android audit first, then iOS
