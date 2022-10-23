<template>
  <v-app id="inspire">
    <v-app-bar
      app
      color="white"
      flat
    >
      <h1 class="ml-16">Home Budget Planner</h1>

      <v-spacer></v-spacer>

      <sign-out-button />
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="2"/>
          <v-col>
            <v-sheet
              min-height="70vh"
              rounded="lg"
            >
              <router-view />
            </v-sheet>
          </v-col>
          <v-col cols="2"/>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import SignOutButton from './components/SignOutButton.vue'
export default {
  components: { SignOutButton },}
</script>