<template>
    <div>
      <div v-if="isLoggedIn">
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
      return this.$store.state.currentUser && this.$store.state.currentUser.username;
    }
  }
}
</script>