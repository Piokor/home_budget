<template>
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn 
          v-bind="attrs"
          v-on="on"
        >
            Create new budget
        </v-btn>
      </template>

      <v-card class="pa-5">
        <v-form
          ref="form"
          v-model="valid"
          class="loginForm"
        >
          <v-text-field
            v-model="title"
            :rules="titleRules"
            label="Title"
            required
          ></v-text-field>

          <v-textarea
            solo
            v-model="description"
            :rules="descriptionRules"
            name="input-7-4"
            label="Budget description"
          ></v-textarea>

          <v-btn @click="createBudget">
            Create budget
          </v-btn>
        </v-form>
      </v-card>
    </v-dialog>    
</template>

<script>
import {createBudget} from '@/api/budgets'
export default {
  data () {
    return {
      dialog: false,
      valid: false,
      title: '',
      titleRules: [
        v => !!v || 'Title is required',
        v => (v && v.length >= 1 && v.length <= 100) || 'Title must be shorter than 100 characters',
      ],
      description: '',
      descriptionRules: [
        v => v.length <= 300 || 'Description must be shorter than 300 characters',
      ],
    }
  },

  methods: {
    async createBudget() {
      this.$refs[`form`].validate();
      if(!this.valid) return;

      const res = await createBudget(this.title, this.description);
      if(res.status == 200) {
        this.dialog = false;
        this.$emit("budgetCreated");
      }
    }
  }
}
</script>