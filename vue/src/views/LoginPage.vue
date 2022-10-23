<template>
  <div>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      color="basil"
      grow
    >
      <v-tab
        v-for="item in tabs"
        :key="item"
      >
        {{ item }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="item in tabs"
        :key="item"
      >
        <div class="d-flex justify-center pa-2">
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
          class="loginForm"
        >
          <v-text-field
            v-model="name"
            :rules="nameRules"
            label="Name"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Password"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="passwordRules"
            :type="showPassword ? 'text' : 'password'"
            name="input-10-1"
            @click:append="showPassword = !showPassword"
          ></v-text-field>

          <v-btn @click="buttonClick">
            {{buttonText}}
          </v-btn>
        </v-form>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
  export default {
    data: () => ({
      valid: true,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length >= 3 && v.length <= 50) || 'Name must be more than 3 and less than 50 characters',
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 3 && v.length <= 50) || 'Password must be more than 3 and less than 50 characters',
      ],
      showPassword: false,
      tabs: ["Login", "Register"],
      tab: null
    }),
    methods: {
      buttonClick() {
        if(this.tab == 0) {
          this.login();
        } else {
          this.signUp();
        }
      },
      login() {

      },
      signUp() {

      }
    },
    computed: {
      buttonText: function () {
        if(this.tab == 0) {
          return "Login"
        } else {
          return "Create account"        
        }
      }
    }
  }
</script>

<style scoped>
.loginForm{
  min-width: 400px;
}
</style>