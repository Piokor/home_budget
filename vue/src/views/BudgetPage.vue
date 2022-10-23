<template>
  <div class="pa-10">
    <BudgetDescription
      v-if="budget"
      :budget="budget"
      class="mb-5"
    />

    <div class="text-h6 mb-4">
      Incomes & Expenses
    
      <v-icon @click="getBudget">
        mdi-refresh
      </v-icon>
    </div>
  
    <TransactionTable
      v-if="budget"
      class="mb-5"
      :transactions="incomes"
      :type="'Incomes'"
    />
  
    <TransactionTable
      v-if="budget"
      :transactions="expenses"
      :type="'Expenses'"
    />
    
    <TransactionCreator 
      :budgetId="budgetId" 
      @transactionCreated="getBudget"
    />
  </div>
</template>

<script>
import {getBudget} from '@/api/budgets'
import BudgetDescription from '../components/BudgetDescription.vue';
import TransactionCreator from '../components/TransactionCreator.vue';
import TransactionTable from '../components/TransactionTable.vue';
export default {
  name: 'App',

  components: {BudgetDescription, TransactionCreator, TransactionTable},

  mounted() {
    if(!this.$route.query.id) {
      this.$router.push("/");
      return;
    }
    this.budgetId = this.$route.query.id;
    this.getBudget();
  },

  data() {
    return {
      budget: null,
      budgetId: null,
      incomes: [],
      expenses: []
    }
  },

  methods: {
    async getBudget() {
      const res = await getBudget(this.budgetId);
      if(res.status == 200) {
        this.budget = res.data;
        this.incomes = res.data.transactions.filter(t => t.type == "income");
        this.expenses = res.data.transactions.filter(t => t.type == "expenses");
      }
    }
  }
};
</script>
