<template>
  <div class="pa-10">
    <BudgetCreator 
      @budgetCreated="getBudgets"
    />

    <BudgetTable 
      :own="true" 
      ref="ownTable"  
      class="mt-4"
    />

    <BudgetTable 
      :own="false" 
      ref="sharedTable" 
      class="mt-4"
    />
  </div>
</template>

<script>
import BudgetCreator from '@/components/BudgetCreator.vue'
import BudgetTable from '@/components/BudgetTable.vue'
export default {
  name: 'App',
  
  components: {BudgetCreator, BudgetTable},

  mounted() {
    if(!this.$store.state.currentUser.token || !this.$store.state.currentUser.token) {
      this.$router.push("/login");
    }
  },

  methods: {
    getBudgets() {
      this.$refs[`ownTable`].getBudgets();
      this.$refs[`sharedTable`].getBudgets();
    }
  }
};
</script>
