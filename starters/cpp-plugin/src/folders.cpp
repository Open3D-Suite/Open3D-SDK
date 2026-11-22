// SPDX-License-Identifier: GPL-3.0-or-later
//
// What OpenExample says about itself (see folders.h).

#include "folders.h"

namespace openexample
{

std::wstring describe(open3d_settings::Language language, const std::optional<std::filesystem::path>& settings,
                      const std::optional<std::filesystem::path>& data)
{
    const bool spanish = language == open3d_settings::Language::Spanish;
    const std::wstring none = spanish ? L"(ninguna carpeta)" : L"(no folder)";
    const auto shown = [&none](const std::optional<std::filesystem::path>& folder) {
        return folder ? folder->wstring() : none;
    };
    std::wstring text = spanish ? L"Idioma: español" : L"Language: English";
    text += spanish ? L"\nAjustes: " : L"\nSettings: ";
    text += shown(settings);
    text += spanish ? L"\nOtros archivos: " : L"\nOther files: ";
    text += shown(data);
    return text;
}

std::wstring describe_here()
{
    return describe(open3d_settings::language(open3d_settings::settings_dir()), open3d_settings::app_settings_dir(kApp),
                    open3d_settings::app_data_dir(kApp));
}

} // namespace openexample
