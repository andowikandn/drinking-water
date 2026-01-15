import allure
from locators.form import FormLocators, SubmitLocators
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class FormPages:
    def __init__(self, page: Page):
        self.page = page

    def verify_form_page(self):
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            expect(
                self.page.locator(FormLocators.header_form_page)
            ).to_be_visible(timeout=10000)

            expect(self.page).to_have_url(
                "https://demoqa.com/automation-practice-form"
            )

        except PlaywrightTimeoutError as e:
            allure.attach(
                self.page.screenshot(),
                name="timeout-error",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(
                "Timeout while waiting for form page to load (domcontentloaded)"
            ) from e
    
    def input_first_name(self, firstname: str):
        with allure.step('User input first name'):
            locator = self.page.locator(FormLocators.first_name_txt)
            locator.fill(firstname)
            expect(locator).to_have_value(firstname)

    def input_last_name(self, lastname: str):
        with allure.step('User input last name'):
            locator = self.page.locator(FormLocators.last_name_txt)
            locator.fill(lastname)
            expect(locator).to_have_value(lastname)

    def input_email(self, email: str):
        with allure.step('User input user email'):
            locator = self.page.locator(FormLocators.user_mail_txt)
            locator.fill(email)
            expect(locator).to_have_value(email)

    def select_gender(self, selectgender: str):
        with allure.step("User select gender"):
            mapping = {
            "Male": "1",
            "Female": "2",
            "Other": "3"
        }
            
        label = self.page.locator(
            FormLocators.gender_label.format(mapping[selectgender])
        )

        label.scroll_into_view_if_needed()
        label.click()

        radio = self.page.locator(
            FormLocators.gender_input.format(mapping[selectgender])
        )

        expect(radio).to_be_checked()

    def input_mobile_number(self, mobilenumber: str):
        with allure.step('User input mobile number'):
            locator = self.page.locator(FormLocators.mobile_number)
            locator.fill(mobilenumber)
            expect(locator).to_have_value(mobilenumber)

    def input_date_of_birth(self, inputdate: str):
        with allure.step('User input date of birth'):
            dob = self.page.locator(FormLocators.set_date_of_birth)
            expect(dob).to_be_visible()
            dob.fill(inputdate)
            expect(dob).to_have_value(inputdate)

    def input_subject(self, subjects: list[str]):
        with allure.step('User input subject'):
            inp_subject = self.page.locator(FormLocators.input_subject)
            expect(inp_subject).to_be_visible()
            
            for subject in subjects:
                inp_subject.fill(subject)
                opt_subject = self.page.locator(f'{FormLocators.subject_opt}:has-text("{subject}")')
                expect(opt_subject).to_be_visible()
                opt_subject.click()

                chip_subject = self.page.locator(f'{FormLocators.subject_chip}:has-text("{subject}")')
                expect(chip_subject).to_be_visible()

    def remova_value_subject(self, removesubject: str):
        with allure.step(f'User remove a value subject {removesubject}'):
            sub_chip = self.page.locator(f'{FormLocators.subject_chip}:has-text("{removesubject}")')
            expect(sub_chip).to_be_visible()

            sub_chip.locator(FormLocators.remove_subject_value).click()
            expect(sub_chip).to_be_hidden()

    def clear_subject(self):
        with allure.step('User clear subject'):
            clear_btn = self.page.locator(FormLocators.clear_subject)
            clear_btn.click()
            expect(clear_btn).to_be_hidden()

    def select_bobbies(self, selecthobbies: list[str]):
        with allure.step('User select hobbies'):
            mapping = {
                "Sports": "1",
                "Reading": "2",
                "Music": "3"
            }

            for hobby in selecthobbies:
                label = self.page.locator(
                    FormLocators.hobbies_label.format(
                        mapping[hobby]))
                label.scroll_into_view_if_needed()
                label.click()

                checkbox = self.page.locator(
                    FormLocators.hobbies_input.format(
                        mapping[hobby]))
                expect(checkbox).to_be_checked()

    def upload_picture(self):
        with allure.step('User upload picture'):
            file_path = '/Users/andowikandono/Desktop/FileImage.png'
            file_input = self.page.locator(FormLocators.upload_picture)
            file_input.set_input_files(file_path)

            value = file_input.input_value()
            assert 'FileImage.png' in value
            
    def input_current_address(self, address: str):
        with allure.step('User input current address'):
            input_address = self.page.locator(FormLocators.current_address_txt)
            input_address.fill(address)
            expect(input_address).to_be_visible()

    def select_state(self, state: str):
        with allure.step(f'User select state {state}'):
            dropdown = self.page.locator(FormLocators.state_dropdown)
            expect(dropdown).to_be_visible(timeout=5000)
            dropdown.click()

            option = self.page.locator(
                f'{FormLocators.select_state}:has-text("{state}")'
            )

            expect(option).to_be_visible(timeout=5000)
            option.click()

            expect(dropdown).to_contain_text(state)

    def select_city(self, city: str):
        with allure.step(f'User select city {city}'):
            dropdown = self.page.locator(FormLocators.city_dropdown)
            expect(dropdown).to_be_visible(timeout=5000)
            dropdown.click()

            option = self.page.locator(
                f'{FormLocators.select_city}:has-text("{city}")'
            )

            expect(option).to_be_visible()
            option.click()

            expect(dropdown).to_contain_text(city)

    def tap_submit_btn(self):
        with allure.step('User click submit button'):
            self.page.locator(FormLocators.submit_btn).click()

    def verify_required_field(self):
        with allure.step('User verify required field'):
            expect(self.page.locator(f'{FormLocators.first_name_txt}:invalid')).to_be_visible(timeout=10000)
            expect(self.page.locator(f'{FormLocators.last_name_txt}:invalid')).to_be_visible(timeout=10000)
            expect(self.page.locator(f'{FormLocators.select_gender}:invalid').first).to_be_visible(timeout=10000)
            expect(self.page.locator(f'{FormLocators.mobile_number}:invalid')).to_be_visible(timeout=10000)
            
    def verify_invalid_field(self):
        with allure.step('User verify invalid field email and mobile number'):
            expect(self.page.locator(f'{FormLocators.user_mail_txt}:invalid')).to_be_visible()
            expect(self.page.locator(f'{FormLocators.mobile_number}:invalid')).to_be_visible()

class SubmitPages:
    def __init__(self, page: Page):
        self.page = page

    def verify_form_modal_page(self):
        with allure.step('User verify header modal page'):
            expect(self.page.locator(SubmitLocators.header_modal)).to_be_visible()
            expect(self.page.locator(SubmitLocators.header_modal)).to_contain_text('Thanks for submitting the form')
            expect(self.page.locator(SubmitLocators.body_modal)).to_be_visible()

    def press_escape(self):
        with allure.step('User press escape'):
            self.page.keyboard.press('Escape')
            expect(self.page.locator(SubmitLocators.body_modal)).to_be_hidden()

    def tap_close_btn(self):
        with allure.step('User close modal button'):
            close_btn = self.page.get_by_role("button", name="Close")
            expect(close_btn).to_be_visible()
            close_btn.wait_for(state='visible')
            close_btn.scroll_into_view_if_needed()
            close_btn.click(force=True)
            expect(self.page.locator(FormLocators.header_form_page)).to_be_visible()