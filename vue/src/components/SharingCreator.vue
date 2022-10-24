<template>
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn 
          v-bind="attrs"
          v-on="on"
          class="mt-5"
        >
            Share budget with a user
        </v-btn>
      </template>

      <v-card class="pa-5">
        <v-form
          ref="form"
          v-model="valid"
          class="loginForm"
        >
          <v-autocomplete
            v-model="username"
            :items="usernamesList"
            :search-input.sync="searchInput"
            label="Username"
          ></v-autocomplete>

          <v-btn class="mt-3" @click="shareBudget">
            Share budget
          </v-btn>
        </v-form>
      </v-card>
    </v-dialog>    
</template>

<script>
import {shareBudget} from '@/api/budgets';
import {getUsers} from '@/api/users';
export default {
  props: ["budgetId"],

  data () {
    return {
      dialog: false,
      valid: false,
      username: '',
      usernameRules: [
        v => !!v || 'username is required'
      ],
      usernamesList: [],
      searchInput: "",
      usersData: null
    }
  },

  methods: {
    async shareBudget(){
      const targetUserId = this.getSelectedUserId()
      const res = await shareBudget(this.budgetId, targetUserId);
      if(res.status == 200) {
        this.dialaog = false;
      }
    },
    async updateUsernameList(){
      if(!this.searchInput) {
        this.usernamesList = [];
        return;
      }
      const res = await getUsers(this.searchInput);
      if(res.status != 200){
        this.usernamesList = [];
        return;
      }
      this.usersData = res.data;
      this.usernamesList = res.data.map(u => u.name);     
    },
    getSelectedUserId(){
      const userData = this.usersData.find(u => u.name == this.username);
      return userData.id;  
    }
  },

  watch: {
    searchInput() {
      this.updateUsernameList();
    }
  }
}
</script>