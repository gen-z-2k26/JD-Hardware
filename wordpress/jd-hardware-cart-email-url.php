<?php
/**
 * Cart abandonment emails: rewrite the WordPress host to the storefront.
 * Paste into Snippets (Run everywhere), or the bottom of the theme functions.php.
 * If WordPress is not on wp.jdhardware.shop, change only the first array.
 * The public shop in the Pages and Policies document is https://jdhardware.shop.
 */

function jd_hardware_ca_rewrite($text) {
    if (!is_string($text) || $text === '') {
        return $text;
    }

    return str_replace(
        array(
            'https://wp.jdhardware.shop',
            'http://wp.jdhardware.shop',
            '//wp.jdhardware.shop',
            'wp.jdhardware.shop',
        ),
        array(
            'https://jdhardware.shop',
            'https://jdhardware.shop',
            '//jdhardware.shop',
            'jdhardware.shop',
        ),
        $text
    );
}

add_filter('wcf_ca_email_body_before_send', 'jd_hardware_ca_rewrite', 20);

add_filter('woo_ca_recovery_email_data', function ($data) {
    if (!is_array($data)) {
        return $data;
    }
    foreach (array('body', 'email_body', 'content', 'checkout_url', 'subject') as $key) {
        if (!empty($data[$key]) && is_string($data[$key])) {
            $data[$key] = jd_hardware_ca_rewrite($data[$key]);
        }
    }
    return $data;
}, 20);

add_filter('wp_mail', function ($args) {
    if (!empty($args['message'])) {
        $args['message'] = jd_hardware_ca_rewrite($args['message']);
    }
    if (!empty($args['subject'])) {
        $args['subject'] = jd_hardware_ca_rewrite($args['subject']);
    }
    return $args;
}, 20);
