<template>  
  <v-card>
    <v-card-title>
      {{title}}
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field> 
      <v-icon @click="getBudgets" class="mt-3 ml-2">
        mdi-refresh
      </v-icon>
    </v-card-title>

    <v-data-table
      :headers="headers"
      :items="budgets"
      :items-per-page="5"
      :no-data-text="noBudgetsMessage"
      :loading="budgetsLoading"
      :search="search"
      class="elevation-1"
    >
      <template v-slot:[`item.actions`]="{ item }">          
        <v-btn 
          @click="viewBudget(item)"
        >
          Details
        </v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>


<script>
import {getBudgets} from '@/api/budgets'
export default {
  props: ["own"],

  mounted() {
    if(!this.own) {
      this.headers.splice(2, 0, {
        text: 'Owner name',
        value: 'owner_name',        
      });
      this.noBudgetsMessage = "No budgets were shared with you"
    }
    this.getBudgets();
  },

  data: () => ({
    headers: [
      {
        text: 'Title',
        align: 'start',
        sortable: true,
        value: 'title',
      },
      {
        text: 'Description',
        value: 'description',
      },
      { text: 'Actions', value: 'actions', sortable: false },
    ],
    budgets: [],
    budgetsLoading: false,
    noBudgetsMessage: "You did not create any budgets",
    search: ""
  }),

  methods: {
    async getBudgets() {
      this.budgetsLoading = true;
      const res = await getBudgets(); 
      this.budgetsLoading = false;
      if(res.status != 200) {
        return;
      }
      if(this.own){
        this.budgets = res.data.own;
      } else {
        this.budgets = res.data.shared;
      }      
    },
    viewBudget(budget) {
      this.$router.push(`/budget?id=${budget["_id"]["$oid"]}`)
    }
  },

  computed: {
    title() {
      if(this.own){
        return "Your budgets";
      } else {
        return "Budgets shared with you"
      }
    }
  }
};
</script>