<template>
  <v-app>

    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-btn to="/" text>Credential Issuer UI</v-btn>
      <v-spacer></v-spacer>

      <v-app-bar-nav-icon />
    </v-app-bar>

    <v-main class="ma-5">
      <nuxt />
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

}
</script>
