---
name: Face ID login
overview: "Đăng nhập nhanh bằng Face ID / Touch ID sẵn có trên iOS (Capacitor Native Biometric + Keychain). Không dùng camera / nhận diện khuôn mặt server."
todos:
  - id: biometric-fe
    content: "FE: BiometricAuthService + nút Face ID trên login + lưu cred sau password login"
    status: completed
  - id: ios-plist
    content: "Info.plist NSFaceIDUsageDescription + npx cap sync ios"
    status: completed
isProject: false
---

# Face ID login (device biometric)

## Cách hoạt động (đơn giản)

1. User login **password** lần đầu trên app iOS.
2. App lưu username/password vào **Keychain** (qua `@capgo/capacitor-native-biometric`).
3. Lần sau mở `/login` → hiện nút **Face ID** (hoặc Touch ID).
4. User quét mặt → OS xác nhận → app lấy cred từ Keychain → gọi API `token` như login thường.

Không cần BE mới. Không camera app. Không enroll khuôn mặt lên server.

## Tắt

Profile → Disable Face ID (xóa cred Keychain trên máy đó).
