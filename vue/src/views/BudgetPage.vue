<template>
  <div class="pa-10">
    <BudgetDescription
      v-if="budget"
      :budget="budget"
      class="mb-5"
      />
    
    <div class="text-h6">
      Incomes & Expenses
    </div>
    
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
export default {
  name: 'App',

  components: {BudgetDescription, TransactionCreator},

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
      budgetId: null
    }
  },

  methods: {
    async getBudget() {
      const res = await getBudget(this.budgetId);
      if(res.status == 200) {
        this.budget = res.data;
      }
    }
  }
};
</script>
