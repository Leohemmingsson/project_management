<template>
    <nav class="navbar">
        <div class="logo">
            <slot name="logo">MyApp</slot>
        </div>
        <div class="nav-right">
            <ul class="nav-links">
                <li v-for="(link, index) in links" :key="index">
                    <router-link :to="link.href">{{ link.text }}</router-link>
                </li>
            </ul>
            <router-link to="/login" class="login-button">Login</router-link>
        </div>
    </nav>
</template>

<script setup>
defineProps({
    links: {
        type: Array,
        required: true,
        default: () => [],
    },
});
</script>

<style scoped>
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: #333;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.logo {
    font-weight: bold;
    font-size: 1.2rem;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 1rem;
    margin: 0;
    padding: 0;
}

.nav-links a {
    color: white;
    text-decoration: none;
}

.login-button {
    background-color: #555;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    transition: background-color 0.3s;
}

.login-button:hover {
    background-color: #777;
}
</style>
