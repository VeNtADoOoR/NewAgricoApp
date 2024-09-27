<template>
    <div class="container mx-auto bg-green-100" style="width: 100%;">
        <AuthNavBar />
        <div class="max-w-4xl mx-auto p-6 bg-green-200 shadow-md rounded-lg">

            <div class="flex justify-center mb-10 relative">
                <div class="relative">
                    <img :src="userPhoto" alt="Profile Picture"
                        class="rounded-full w-32 h-32 object-cover border-4 border-gray-300" />
                    <button @click="triggerFileInput"
                        class="absolute bottom-0 right-0 bg-green-700 text-white p-2 rounded-full shadow-md hover:bg-green-500 transition duration-200">
                        Edit
                    </button>

                    <!-- Hidden file input -->
                    <input type="file" ref="fileInput" @change="handleFileChange" class="hidden" accept="image/*">
                </div>
            </div>

            <!-- First Name & Last Name Section -->
            <form class="mb-6" @submit.prevent="updateName">
                <h2 class="text-lg font-semibold mb-4">Edit full name</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input type="text" v-model="firstName" placeholder="First Name"
                        class="border border-gray-300 p-2 rounded-md w-full" />
                    <input type="text" v-model="lastName" placeholder="Last Name"
                        class="border border-gray-300 p-2 rounded-md w-full" />
                </div>
                <button type="submit"
                    class="mt-4 bg-green-700 text-white py-2 px-6 rounded-md hover:bg-green-500 transition duration-200">
                    Save
                </button>
            </form>

            <!-- Email Section -->
            <form class="mb-6" @submit.prevent="updateEmail">
                <h2 class="text-lg font-semibold mb-4">Edit Email</h2>
                <input type="email" v-model="email" placeholder="Email Address"
                    class="border border-gray-300 p-2 rounded-md w-full" />
                <button type="submit"
                    class="mt-4 bg-green-700 text-white py-2 px-6 rounded-md hover:bg-green-500 transition duration-200">
                    Verify
                </button>
            </form>

            <!-- Password Section -->
            <form class="mb-8" @submit.prevent="updatePassword">
                <h2 class="text-lg font-semibold mb-4">Change Password</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <input type="password" v-model="currentPassword" placeholder="Current Password"
                        class="border border-gray-300 p-2 rounded-md w-full" />
                    <input type="password" v-model="newPassword" placeholder="New Password"
                        class="border border-gray-300 p-2 rounded-md w-full" />
                    <input type="password" v-model="newPasswordConfirmation" placeholder="Confirm Password"
                        class="border border-gray-300 p-2 rounded-md w-full" />
                </div>
                <button type="submit"
                    class="mt-4 bg-green-700 text-white py-2 px-6 rounded-md hover:bg-green-500 transition duration-200">
                    Save
                </button>
            </form>

            <!-- Two Factor Authentication -->
            <TwoFactorAuthenticationForm />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { usePage } from '@inertiajs/vue3';
import TwoFactorAuthenticationForm from '@/Components/TwoFactorAuthenticationForm.vue';
import AuthNavBar from '@/Components/AuthNavBar.vue';
import axios from 'axios';

// Form data
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const id = ref('');
const currentPassword = ref('');
const newPassword = ref('');
const newPasswordConfirmation = ref('');
const fileInput = ref(null);

// Fetch authenticated user data
const { props } = usePage();
const user = props.auth.user;
const userPhoto = ref(user?.profile_photo_path ? `${window.location.origin}/storage/${user.profile_photo_path}` : '/images/default-user-photo.jpg');

// Method to trigger the hidden file input
const triggerFileInput = () => {
    fileInput.value.click();  // Simulate a click on the file input
};



// Prefill form fields with user data on component mount
onMounted(() => {
    firstName.value = user?.first_name || '';
    lastName.value = user?.last_name || '';
    email.value = user?.email || '';
    id.value = user?.id;
});

// Methods
const updateName = async () => {
    try {
        // Send firstName and lastName as payload in the PUT request
        const nameResponse = await axios.put(`/api/user/${id.value}/update-name`, {
            agr_fname: firstName.value, // Send firstName as agr_fname
            agr_lname: lastName.value,  // Send lastName as agr_lname
        });

        alert('Name updated successfully');
    } catch (error) {
        console.error('Error updating name:', error);
    }
};

const updateEmail = async () => {
    try {
        // Make a request to update the email
        const response = await axios.post('/api/user/update-email', {
            email: email.value,
        });

        // Handle success
        alert(response.data.message || 'Email updated successfully.');

    } catch (error) {
        // Handle errors
        if (error.response && error.response.data) {
            // Show the specific error message returned from the server
            alert(error.response.data.message || 'An error occurred.');
        } else {
            alert('An unexpected error occurred.');
        }
    }
};



const updatePassword = async () => {
    // Validate the current password
    if (!currentPassword.value) {
        alert("Please enter your current password.");
        return;
    }

    // Validate the new password
    if (!newPassword.value) {
        alert("Please enter a new password.");
        return;
    }

    // Validate confirmation of new password
    if (newPassword.value !== newPasswordConfirmation.value) {
        alert("New password and confirmation do not match.");
        return;
    }

    // Assuming you have an endpoint for updating the password
    try {
        const response = await axios.put(`/api/user/${id.value}/update-password`, {
            current_password: currentPassword.value,
            new_password: newPassword.value,
            new_password_confirmation: newPasswordConfirmation.value
        });

        // Handle successful response
        if (response.status === 200) {
            alert("Password updated successfully!");
            // Clear the password fields after successful update
            currentPassword.value = '';
            newPassword.value = '';
            newPasswordConfirmation.value = '';
        }
    } catch (error) {
        // Handle errors, such as incorrect current password
        if (error.response && error.response.status === 422) {
            alert("Current password is incorrect.");
        } else {
            alert("An error occurred while updating the password.");
        }
    }
};


const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('profile_photo', file);

        try {
            const response = await axios.post(`/api/user/${id.value}/update-photo`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // Update userPhoto with the returned URL
            userPhoto.value = response.data.profile_photo_path; // This should be a full URL now
        } catch (error) {
            console.error('Error uploading photo:', error);
        }
    }
};


</script>


<style scoped>
/* Additional styles can be added if needed */
</style>