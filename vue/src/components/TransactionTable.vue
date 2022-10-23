<template>  
  <v-card>
    <v-card-title>
      {{type}}
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field> 
    </v-card-title>

    <v-data-table
      :headers="headers"
      :items="transactions"
      :items-per-page="5"
      :no-data-text="`This budget does't have any ${type}`"
      group-by="category"
      :search="search"
      class="elevation-1"
    />
  </v-card>
</template>


<script>
export default {
  props: ["transactions", "type"],

  mounted() {
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
        text: 'Amount',
        value: 'amount',
      },
      {
        text: 'Currency',
        value: 'currency',
      },
      { text: 'Category', value: 'category', align: 'right' }
    ],
    search: ""
  }),

  methods: {
    
  }
};
</script>