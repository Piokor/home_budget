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

          <p v-if="errorMessageOn" style="color:red; font-size: 0.85em;">
            {{errorMessage}}
          </p>
        </v-form>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import {register, login} from '@/api/login'
export default {
  mounted() {
    this.$store.commit('signOff');
  },
  data: () => ({
    valid: false,
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
    tabs: ["Register", "Login"],
    tab: null,
    errorMessageOn: false,
    failMessage: ""
  }),
  methods: {
    buttonClick() {
      this.errorMessageOn = false;
      this.$refs[`form`][0].validate();
      if(!this.valid) return;
    
      if(this.currentTab == "login") {
        this.login();
      } else {
        this.signUp();
      }
    },

    async login() {
      const res = await login(this.name, this.password);
      if(res.status != 200) {
        this.handleFail(res);
        return;
      }
      this.$store.commit('setCurrentUser', {
        token: res.data.token,
        username: this.name
      });
      this.$router.push("/");
    },
    
    async signUp() {
      const res = await register(this.name, this.password);
      if(res.status != 200) {
        this.handleFail(res);
      } else {
        this.login();
      }
    },

    handleFail(response){
      this.failMessage = response.data;
      this.errorMessageOn = true;
    }
  },
  computed: {
    currentTab: function () {
      if(this.tab == 0) {
        return "register"
      } else {
        return "login"        
      }
    },
    buttonText: function () {
      if(this.currentTab == "login") {
        return "Login"
      } else {
        return "Create account"        
      }
    },
    errorMessage: function () {
      if(this.currentTab == "login" ) {
        return `Could not log in (${this.failMessage})`
      } else {
        return `Could not create account (${this.failMessage})`
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