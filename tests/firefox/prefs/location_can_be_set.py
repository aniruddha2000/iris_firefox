# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Cookies and Site Data can be managed via the "Managed Cookies and Site Data" panel.',
        test_case_id='143633',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        save_changes_button_pattern = AboutPreferences.Privacy.Exceptions.SAVE_CHANGES_BUTTON
        refresh_page_pattern = NavBar.RELOAD_BUTTON

        browser_privacy_hover_pattern = Pattern('browser_privacy_hover.png')
        show_location_button_pattern = Pattern('show_location_button.png').exact()
        allow_location_access_pattern = Pattern('allow_location_access.png')
        remember_decision_pattern = Pattern('remember_decision.png')
        location_settings_label_pattern = Pattern('location_settings_label.png')
        google_maps_tab_pattern = Pattern('google_maps_tab.png')
        settings_button_pattern = Pattern('settings_button.png')
        google_location_allowed_pattern = Pattern('google_with_allowed_location.png')
        google_location_blocked_pattern = Pattern('google_with_blocked_location.png')
        allow_button_pattern = Pattern('allow_button.png')
        google_maps_no_location_permissions_close_button_pattern = \
            Pattern('google_maps_no_location_permissions_message.png').exact()

        scroll_length = Screen.SCREEN_WIDTH // 3
        if OSHelper.is_linux():
            scroll_length = 5
        if OSHelper.is_mac():
            scroll_length = 10

        navigate('about:preferences#privacy')

        browser_privacy_label_exists = exists(browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_privacy_label_exists, "The options for \"Privacy & Security\" section are displayed"

        hover(browser_privacy_hover_pattern)
        scroll_until_pattern_found(location_settings_label_pattern, scroll, (-scroll_length,), 30)

        new_tab()

        navigate('google.com/maps')

        google_maps_tab_opened = exists(google_maps_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_maps_tab_opened, "Google maps website is opened"

        show_location_button_exists = exists(show_location_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                             region=Screen.bottom_half(Screen.right_half(Screen.RIGHT_HALF)))
        assert show_location_button_exists, "Location request can be invoked"

        click(show_location_button_pattern, Settings.DEFAULT_SLOW_MOTION_DELAY)

        allow_location_access_exists = exists(allow_location_access_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert allow_location_access_exists, "A notification is displayed asking permission to access your location."

        click(remember_decision_pattern)
        click(allow_location_access_pattern)

        previous_tab()

        location_loc = find(location_settings_label_pattern)
        location_loc_x, location_loc_y = location_settings_label_pattern.get_size()
        location_loc_region = Rectangle(location_loc.x, location_loc.y - 10, location_loc_x * 10, location_loc_y + 10)

        settings_label_found = exists(settings_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT, location_loc_region)
        assert settings_label_found, "Settings can be opened for location"

        click(settings_button_pattern, region=location_loc_region)

        google_location_allowed = exists(google_location_allowed_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_location_allowed, "The visited site is listed and it has the status \"Allow\""
        click(save_changes_button_pattern)

        next_tab()
        click(refresh_page_pattern)

        google_maps_tab_opened = exists(google_maps_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_maps_tab_opened, "Google maps website is opened"

        show_location_button_exists = exists(show_location_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                             region=Screen.bottom_half(Screen.right_half(Screen.RIGHT_HALF)))
        assert show_location_button_exists, "Location request can be invoked"

        click(show_location_button_pattern, Settings.DEFAULT_SLOW_MOTION_DELAY)

        allow_location_access_exists = not exists(allow_location_access_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert allow_location_access_exists, "The notification is not displayed "  # and the location is found."
        # consider maybe we should add here check whether location was found (correctly found)

        previous_tab()

        settings_label_found = exists(settings_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT, location_loc_region)
        assert settings_label_found, "Settings can be opened for location"

        click(settings_button_pattern, region=location_loc_region)

        google_location_allowed = exists(google_location_allowed_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_location_allowed, "The visited site is listed and it has the status \"Allow\""

        click(allow_button_pattern)
        type(Key.DOWN)  # select block from list
        type(Key.ENTER)

        google_location_blocked = exists(google_location_blocked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_location_blocked, "Location usage is now blocked for site."

        click(save_changes_button_pattern)

        next_tab()

        click(refresh_page_pattern)

        google_maps_tab_opened = exists(google_maps_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_maps_tab_opened, "Google maps website is opened"

        show_location_button_exists = exists(show_location_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                             region=Screen.bottom_half(Screen.right_half(Screen.RIGHT_HALF)))
        assert show_location_button_exists, "Location request can be invoked"

        click(show_location_button_pattern, Settings.DEFAULT_SLOW_MOTION_DELAY)

        you_blocked_permissions_popup_displayed = exists(google_maps_no_location_permissions_close_button_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert you_blocked_permissions_popup_displayed, "The message \"Google Maps does not have permission to use " \
                                                        "your location.\" is displayed at the bottom of the page. "

        previous_tab()

        settings_label_found = exists(settings_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT, location_loc_region)
        assert settings_label_found, "Settings can be opened for location"

        click(settings_button_pattern, region=location_loc_region)

        block_new_requests_checkbox_exists = exists(AboutPreferences.UNCHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert block_new_requests_checkbox_exists, "Block new requests asking to access your location is unchecked"

        click(AboutPreferences.UNCHECKED_BOX)

        click(save_changes_button_pattern)

        next_tab()

        click(refresh_page_pattern)

        google_maps_tab_opened = exists(google_maps_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_maps_tab_opened, "Google maps website is opened"

        show_location_button_exists = exists(show_location_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                             region=Screen.bottom_half(Screen.right_half(Screen.RIGHT_HALF)))
        assert show_location_button_exists, "Location request can be invoked"

        click(show_location_button_pattern, Settings.DEFAULT_SLOW_MOTION_DELAY)

        you_blocked_permissions_popup_displayed = exists(google_maps_no_location_permissions_close_button_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert you_blocked_permissions_popup_displayed, "The message \"Google Maps does not have permission to use " \
                                                        "your location.\" is displayed at the bottom of the page. "