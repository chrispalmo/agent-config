# Device frame sources

Discovery notes checked 13 November 2026. These are starting points, not a complete model inventory or a guarantee of continued maintenance. Recheck the exact asset and its terms when selecting it. No third-party frame assets are bundled with this skill.

## Official artwork and geometry

| Source | Useful for | Limits to check |
| --- | --- | --- |
| [Apple Design Resources — Product Bezels](https://developer.apple.com/design/resources/#product-bezels) | Official Photoshop/PNG product artwork; the checked page includes iPhone 16. | Select the actual variant in the download. Follow the linked usage guidance; availability is not a blanket redistribution license. |
| [Apple accessory resources](https://developer.apple.com/accessories/) and [iPhone 16 dimensional drawing](https://developer.apple.com/download/files/accessories/dimensional-drawings/iphone-16.pdf) | Checking physical geometry when adapting or constructing a frame. | A drawing is reference material, not a ready-to-use transparent mockup. Read its dimensions and terms directly. |
| [Android Device Art Generator](https://developer.android.com/distribute/marketing-tools/device-art-generator) | Google's screenshot-framing tool for available devices. | Check its current model selector; it does not claim every Android phone. Its page excludes generated artwork from Google Play listing screenshots/feature images. |
| [Android Studio screenshot editor](https://developer.android.com/studio/debug/am-screenshot.html) | Framing a native screenshot in an existing Android development workflow. | Its documentation warns that selecting another device's frame stretches the screenshot. Use a matching capture and frame. |

For example, [Apple's iPhone 16 specifications](https://www.apple.com/iphone-16/specs/) identify a 1179 × 2556 pixel display and Dynamic Island. A candidate that calls itself iPhone 16 but uses a notch fails that model check. These pixel dimensions do not by themselves verify browser or native logical coordinates.

## Reusable cross-platform sources

| Source | Available representation | Selection notes |
| --- | --- | --- |
| [Open Device Frame](https://github.com/SinaKarimi7/open-device-frame) · [catalog](https://open-device-frame.vercel.app/) · [API documentation](https://open-device-frame.vercel.app/api-docs) | Transparent black front-view WebP illustrations, with model metadata and a read API. The checked landing page advertised 50 devices across Apple, Google, Huawei, Samsung, and Xiaomi. The repository declares MIT. | A useful broad lookup candidate, with community artwork rather than manufacturer certification. Verify the exact record, asset quality, screen opening, and license at the chosen commit. The count is a dated observation, not a completeness claim. |
| [Telephone](https://github.com/sneas/telephone) · [demo](https://sneas.github.io/telephone/) | MIT SVG web components that wrap live HTML; documented phone elements include `iphone-16-max` and `pixel-9-pro`. | Small model set. The iPhone element name does not establish that it represents the base iPhone 16 or precisely identify an Apple variant. Inspect its geometry before choosing it; verify orientation behavior separately. |
| [Devices.css](https://github.com/picturepan2/devices.css) · [demo](https://devicescss.xyz/) | MIT CSS device shells, including iPhone 14/14 Pro, Pixel/Pixel 2 XL, and Galaxy S8 in the checked README. | Useful for matching older models. The checked README lists landscape and responsive support as future work. Do not relabel an older shell as a newer phone. |
| [MockUPhone](https://mockuphone.com/) | Screenshot mockup generator with iPhone and Android choices, including Galaxy S24 Ultra on the checked home page. | An output tool rather than an assumed redistributable code library. Verify the selected device and asset attribution/terms; using it must not imply permission to upload private screenshots. |

For Open Device Frame, the documented discovery shape is `GET /api/v1/resolve?model=<URL-encoded exact model>`, with `GET /api/v1/search?q=<query>` for candidates. Read the returned identity and match type before selecting `images.frontOff`; a partial match is not an exact match. Repository records live under `catalog/devices/` and artwork under `public/devices/`. Do not infer an unobserved asset path from a marketing name. The API response is not documented as a complete screen-placement or safe-area specification; inspect the asset and supply those coordinates separately.

## Known selection traps

The checked [mobile-device-frames device table](https://github.com/phucsystem/mobile-device-frames#device-options) groups iPhone 16/15/14 under a 390 × 844 notched preset, contrary to the base iPhone 16's published display and cutout. This is a concrete reason to check a library's assets and model metadata rather than accept its fidelity claim. Recheck if the upstream project corrects it; do not treat this dated finding as a permanent judgment of the project.

The historical [Meta device resources URL](https://design.facebook.com/toolsandresources/devices/) returned a Facebook block page during this check. It was not verified as a usable current catalog. Do not make it a required dependency based on older recommendations.

A Figma frame-size preset, browser device-emulation preset, or viewport-size database does not supply the phone's exterior artwork. Conversely, a convincing bezel does not verify a viewport, safe areas, or platform behavior. Keep those claims separate.
