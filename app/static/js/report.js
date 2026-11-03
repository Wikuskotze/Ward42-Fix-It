document.addEventListener("DOMContentLoaded", () => {

    const description =
        document.getElementById("description");

    const counter =
        document.getElementById("descriptionCount");

    const photoInput =
        document.getElementById("photo");

    const preview =
        document.getElementById("photoPreview");

    const form =
        document.getElementById("reportForm");

    const errorBox =
        document.getElementById("formErrors");

    const saveDraftButton =
        document.getElementById("saveDraftBtn");

    const categoryField =
        document.getElementById("category");

    const streetField =
        document.getElementById("street");

    const cellField =
        document.getElementById("reporter_cell");

    // Character Counter

    if (description && counter) {

        description.addEventListener("input", () => {

            counter.textContent =
                `${description.value.trim().length} / 500 characters`;

        });

    }

    // Photo Preview

    if (photoInput && preview) {

        photoInput.addEventListener("change", event => {

            const file =
                event.target.files[0];

            if (!file) return;

            if (errorBox) {

                errorBox.classList.add("d-none");

                errorBox.textContent = "";

            }

            const allowedTypes = [
                "image/jpeg",
                "image/png"
            ];

            if (!allowedTypes.includes(file.type)) {

                if (errorBox) {

                errorBox.textContent =
                    "Only JPG and PNG files are allowed.";

                errorBox.classList.remove("d-none");

                }

                photoInput.value = "";

                preview.classList.add("d-none");

                return;
            }

            if (file.size > 2 * 1024 * 1024) {

                if (errorBox) {

                errorBox.textContent =
                    "Photo exceeds the 2 MB limit.";

                errorBox.classList.remove("d-none");

                }

                photoInput.value = "";

                preview.classList.add("d-none");

                return;
            }

            const reader =
                new FileReader();

            reader.onload = e => {

                preview.src = e.target.result;

                preview.classList.remove("d-none");

                if (errorBox) {

                    errorBox.classList.add("d-none");

                    errorBox.textContent = "";
                }

            };

            reader.readAsDataURL(file);

        });

    }

    // Form Validation

    if (form && errorBox && description) {

        form.addEventListener("submit", event => {

            const descriptionText =
                description.value.trim();

            let isValid = true;

            errorBox.classList.add("d-none");
            errorBox.textContent = "";

            if (descriptionText.length < 10) {

                isValid = false;

                errorBox.textContent =
                    "Description must contain at least 10 characters.";
            }

            if (descriptionText.length > 500) {

                isValid = false;

                errorBox.textContent =
                    "Description may not exceed 500 characters.";
            }

            if (categoryField && !categoryField.value) {

                isValid = false;

                errorBox.textContent =
                    "Please select a category.";
            }

            if (streetField && streetField.value.trim().length < 3) {

                isValid = false;

                errorBox.textContent = 
                    "Street name must contain at least 3 characters.";
            }

            const cellPattern =
                /^0[0-9]{9}$/;

            if (cellField && !cellPattern.test(cellField.value.trim())) {

                isValid = false;

                errorBox.textContent =
                    "Please enter a valid 10-digit South African cellphone number.";
            }

            if (!isValid) {

                event.preventDefault();

                errorBox.classList.remove("d-none");

                errorBox.focus();

                return;

            }

            localStorage.removeItem("faultDraft");

        });

    }

    // Save Draft

    if (saveDraftButton) {

        saveDraftButton.addEventListener("click", () => {

            const draft = {

                category:
                    categoryField ? categoryField.value : "",

                street:
                    streetField ? streetField.value : "",

                description:
                    description ? description.value : ""

            };

            localStorage.setItem(
                "faultDraft",
                JSON.stringify(draft)
            );

            const draftMessage = 
                document.getElementById("draftMessage");

            if (draftMessage) {

                draftMessage.textContent =
                    "Draft saved successfully.";

                draftMessage.classList.remove("d-none");

                setTimeout(() => {

                    draftMessage.classList.add("d-none");

                    draftMessage.textContent = "";

                }, 3000);

            }

        });

    }

    // Load Draft

    const savedDraft =
        localStorage.getItem("faultDraft");

    if (savedDraft) {

        try {

        const draft =
            JSON.parse(savedDraft);

        if (categoryField) {

            categoryField.value =
                draft.category || "";
        }

        if (streetField) {

            streetField.value =
                draft.street || "";
        }

        if (description) {

            description.value =
                draft.description || "";
        }

        if (draft.description && counter) {

            counter.textContent =
                `${draft.description.trim().length} / 500 characters`;

        }

    } catch {

        localStorage.removeItem(
            "faultDraft"
        );
    }

    }

});
