function xytorgb (x, y, bright_int_ret) {
    var z = (1 - x - y);
    var Y = (bright_int_ret/254);
    var X = ((Y / y) * x);
    var Z = ((Y / y) * z);
    var r = ((X * 1.4628067) - (Y * 0.1840623) - (Z * 0.2743606));
    var g = ((-X * 0.5217933) + (Y * 1.4472381) + (Z * 0.0677227));
    var b = ((X * 0.0349342) - (Y * 0.0968930) + (Z * 1.2884099));
    if (r <= 0.0031308) {var r_gamma = (r * 12.92)} else {var r_gamma = ((1.0 + 0.055) * (r ** (1.0 / 2.4)) - 0.055)};
    if (g <= 0.0031308) {var g_gamma = (g * 12.92) * 254} else {var g_gamma = ((1.0 + 0.055) * (g ** (1.0 / 2.4)) - 0.055)};
    if (b <= 0.0031308) {var b_gamma = (b * 12.92) * 254} else {var b_gamma = ((1.0 + 0.055) * (b ** (1.0 / 2.4)) - 0.055)};
    if (r_gamma > 1){var r_gamma_254 = 254} else {var r_gamma_254 = Math.round (r_gamma * 254)};
    if (g_gamma > 1){var g_gamma_254 = 254} else {var g_gamma_254 = Math.round (g_gamma * 254)};
    if (b_gamma > 1){var b_gamma_254 = 254} else {var b_gamma_254 = Math.round (b_gamma * 254)};
    return {r_gamma_ret: r_gamma_254, g_gamma_ret: g_gamma_254, b_gamma_ret: b_gamma_254}}