document.addEventListener("DOMContentLoaded", () => {

    const password =
        document.getElementById("password");

    const checkbox =
        document.getElementById("showPassword");

    const label =
        document.getElementById("showPasswordLabel");

    if (!password || !checkbox) return;

    checkbox.addEventListener("change", () => {

        password.type =
            checkbox.checked
                ? "text"
                : "password";

        checkbox.setAttribute(
            "aria-checked",
            checkbox.checked
        );

        if (label) {

            label.textContent =
                checkbox.checked
                    ? "Hide Password"
                    : "Show Password";
        }

    });

});
