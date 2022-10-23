<template>
    <div>
      <div v-if="$store.state.currentUser && $store.state.currentUser.username">
        <v-icon>
          mdi-account
        </v-icon>
        <span class="mr-5">{{$store.state.currentUser.username}}</span>
        <v-btn
          @click="signOut"
        >
          Sign out
        </v-btn>
      </div>
    </div>
</template>

<script>
export default {
  methods: {
    signOut() {
      this.$store.commit('signOff');
      this.$router.push('/login');
    },
    isLoggedIn() {
      return this.$store.state.currentUser != null && this.$store.state.currentUser.username != null;
    }
  }
}
</script>