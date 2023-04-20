function dataRender() {
    var select = document.getElementById("selectCountry");
    var selectedOption = select.options[select.selectedIndex];
    var countryCode = selectedOption.getAttribute("data-countryCode");
    var displayText = selectedOption.text;
    var country_code = document.getElementById("country_code");
    country_code.value = countryCode;
    var display_text = document.getElementById("country_code_name");
    display_text.value = displayText;
    var select = document.getElementById("selectState");
    var selectedOption = select.options[select.selectedIndex];
    var displayText = selectedOption.text;
    var display_text = document.getElementById("driving_license_country_code_name");
    display_text.value = displayText;

}