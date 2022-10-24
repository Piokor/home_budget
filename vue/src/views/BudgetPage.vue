<template>
  <div class="pa-10">
    <div v-if="budget">
      <BudgetDescription
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
        class="mb-5"
        :transactions="incomes"
        :type="'Incomes'"
      />
    
      <TransactionTable
        :transactions="expenses"
        :type="'Expenses'"
      />
      
      <TransactionCreator 
        v-if="isOwnBudget"
        :budgetId="budgetId" 
        @transactionCreated="getBudget"
      />
      
      <SharingCreator 
        v-if="isOwnBudget"
        :budgetId="budgetId"
      />
    </div>

    <p style="color:red; font-size: 0.85em;">
      {{errorMessage}}
    </p>
  </div>
</template>

<script>
import {getBudget} from '@/api/budgets'
import BudgetDescription from '../components/BudgetDescription.vue';
import TransactionCreator from '../components/TransactionCreator.vue';
import TransactionTable from '../components/TransactionTable.vue';
import SharingCreator from '../components/SharingCreator.vue';
export default {
  name: 'App',

  components: {BudgetDescription, TransactionCreator, TransactionTable, SharingCreator},

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
      expenses: [],
      isOwnBudget: false,
      errorMessage: ""
    }
  },

  methods: {
    async getBudget() {
      this.errorMessage = "";
      const res = await getBudget(this.budgetId);
      if(res.status == 200) {
        this.budget = res.data;
        this.incomes = res.data.transactions.filter(t => t.type == "income");
        this.expenses = res.data.transactions.filter(t => t.type == "expense");
        this.isOwnBudget = 
          this.$store.state.currentUser.username == this.budget.owner_name;
      } else {
        this.errorMessage = res.data;
      }
    }
  }
};
</script>
