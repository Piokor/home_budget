<template>  
  <div>
    <div class="text-h3">
      Budget: {{budget.title}}
    </div>

    <div class="text-caption" v-if="budget.owner_name">
      Owner: {{budget.owner_name}}
    </div>

    <div class="text-subtitle-2">
      {{budget.description}}
    </div>

    <div v-if="Object.keys(balances).length">
      <div class="text-h-4 mt-5">
        Balances:
      </div>
      <div 
        v-for="(balance, index) in balances" 
        :key="index"
        class="text-body-2"
      >
        {{index}}: {{balance}}
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ["budget"],

  data() {
    return {
      balances: null
    }
  },

  methods: {
    computeBalance() {
      // compute balance in each present currency
      const balances = {}
      for(const transaction of this.budget.transactions) {
        if(balances[transaction.currency] == null){
          balances[transaction.currency] = 0;
        }
        if(transaction.type == "expense") {
          balances[transaction.currency] -= transaction.amount;
        } else if(transaction.type == "income") {
          balances[transaction.currency] += transaction.amount;
        }
      }

      for(const i in balances) {        
        if (balances[i] > 0) {
          // parse to str add a + sign before for readability
          balances[i] = "+" + balances[i];
        }
      }

      this.balances = balances;
    }
  },

  watch: {    
    budget: {
      handler() {
        this.computeBalance()
      },
      immediate: true,
      deep: true
    }
  }
};
</script>