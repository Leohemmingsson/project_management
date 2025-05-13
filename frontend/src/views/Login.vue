<template>
    <form @submit.prevent="handleLogin">
        <input v-model="username" placeholder="Username" required />
        <input
            v-model="password"
            type="password"
            placeholder="Password"
            required
        />
        <button type="submit">Login</button>
        <p v-if="error">{{ error }}</p>
    </form>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "../composables/useAuth";

const { login, error } = useAuth();
const username = ref("");
const password = ref("");

const handleLogin = async () => {
    const success = await login(username.value, password.value);
    if (success) {
        // Navigate or close modal
    }
};
</script>
