// SPDX-License-Identifier: GPL-3.0-or-later
//
// What OpenExample says about itself: where it keeps its files, in the language every Open3D app shares.
// Plain C++ with no 3ds Max header, so that it builds and is tested without the 3ds Max SDK.

#pragma once

#include "open3d_settings.h"

#include <filesystem>
#include <optional>
#include <string>

namespace openexample
{

// The app's name, as the Open3D launcher shows it and as its folders are called.
inline constexpr const wchar_t* kApp = L"OpenExample";

// The language, the folder of the app's settings and the folder of everything else it writes, one per
// line, in that language. A missing folder is said. Nothing is created.
std::wstring describe(open3d_settings::Language language, const std::optional<std::filesystem::path>& settings,
                      const std::optional<std::filesystem::path>& data);

// describe() for this computer: the shared language and OpenExample's two folders,
// %APPDATA%\Open3D\OpenExample and %LOCALAPPDATA%\Open3D\OpenExample, or OpenExample in the folders that
// OPEN3D_SETTINGS_DIR and OPEN3D_DATA_DIR name.
std::wstring describe_here();

} // namespace openexample
