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
            Create new Income/Expense
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

          <v-select
            v-model="type"
            :items="['Income', 'Expense']"
            :rules="typeRules"
            label="Type"
          ></v-select>

          <v-select
            v-model="category"
            :items="transactionCategories"
            :rules="categoryRules"
            label="Category"
          ></v-select>

          <div class="d-flex">
            <v-text-field
              v-model="amount"
              :rules="amountRules"
              label="Money amount (monthy)"
              required
            ></v-text-field>  

            <v-select
              v-model="currency"
              :items="['USD', 'EURO', 'PLN']"
              :rules="currencyRules"
              label="Currency"
              class="ml-4"
            ></v-select>
          </div>

          <v-btn @click="createBudget" class="mt-3">
            Create {{type}}
          </v-btn>
        </v-form>
      </v-card>
    </v-dialog>    
</template>

<script>
import {createTransaction} from '@/api/transaction'
export default {
  props: ["budgetId"],

  data () {
    return {
      dialog: false,
      valid: false,
      title: '',
      titleRules: [
        v => !!v || 'Title is required',
        v => (v && v.length >= 1 && v.length <= 200) || 'Title must be shorter than 200 characters',
      ],
      type: '',
      typeRules: [v => !!v || 'Type is required'],
      amount: '',
      amountRules: [
        v => !!v || 'Amount is required',
        v => (v && !isNaN(parseFloat(v))) || 'Amount must be a number',
        v => (v && (v.split(".").length == 1 || v.split(".")[1].length <= 2)) || `Amount can't have more than 2 decimal places`
      ],
      category: '',
      categoryRules: [v => !!v || 'Category is required (select type first)'],
      currency: '',
      currencyRules: [v => !!v || 'Currency is required'],
    }
  },

  methods: {
    async createBudget() {
      this.$refs[`form`].validate();
      if(!this.valid) return;

      const res = await createTransaction({
        title: this.title,
        type: this.type.toLowerCase(),
        category: this.category,
        amount: parseFloat(this.amount),
        currency: this.currency,
        budget_id: this.budgetId
      });
      if(res.status == 200) {
        this.dialog = false;
        this.$emit("transactionCreated");
      }
    }
  },

  computed: {
    transactionCategories() {
      if(this.type == "Income") {
        return ["Salary", "Tips", "Passive"]
      } else if (this.type == "Expense") {
        return ["Utilities", "Food", "Personal"]
      } else {
        return [];
      }
    }
  }
}
</script>