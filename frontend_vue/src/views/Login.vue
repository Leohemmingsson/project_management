<template>
    <div class="min-h-screen flex items-center justify-center">
        <form
            @submit.prevent="handleLogin"
            class="bg-white p-8 rounded-xl shadow-md w-full max-w-sm space-y-6"
        >
            <h2 class="text-2xl font-semibold text-gray-900 text-center">
                Login
            </h2>

            <div class="space-y-4">
                <input
                    v-model="username"
                    type="text"
                    placeholder="Username"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder-gray-600 bg-white text-gray-900"
                />

                <input
                    v-model="password"
                    type="password"
                    placeholder="Password"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder-gray-600 bg-white text-gray-900"
                />
            </div>

            <button
                type="submit"
                class="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition duration-200"
            >
                Login
            </button>

            <p v-if="error" class="text-red-600 text-sm text-center mt-2">
                {{ error }}
            </p>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "../composables/useAuth";
import { useRouter } from "vue-router";

const { login, error } = useAuth();
const username = ref("");
const password = ref("");

const router = useRouter();

const handleLogin = async () => {
    const success = await login(username.value, password.value);
    if (success) {
        router.push("/");
    }
};
</script>
