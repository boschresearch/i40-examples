<!--
 Copyright (c) 2021 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/IDunion/i40-examples

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <div>
    <v-text-field label="First Name" v-model="first_name" :disabled="lock"></v-text-field>
    <v-text-field label="Last Name" v-model="last_name" :disabled="lock"></v-text-field>
    <v-text-field label="Email" v-model="email" :disabled="lock"></v-text-field>
    <v-btn @click="requestCredential()" color="primary" :disabled="lock"><v-icon>mdi-send</v-icon>Send</v-btn>

    <v-btn @click="logout()" color="primary"><v-icon>mdi-logout</v-icon>Logout</v-btn>

    <v-alert type="error" v-if="error">{{error}}</v-alert>
    <v-alert type="success" v-if="message">{{message}}</v-alert>
    <br />
    <vue-qrcode v-if="invitation_url" :value="invitation_url" />
  </div>
</template>

<script>
import VueQrcode from 'vue-qrcode'
export default {
  components: {
    VueQrcode
  },

  data () {
    return {
      lock: false,
      first_name: '',
      last_name: '',
      email: '',
      error:'',
      message: '',
      invitation_url:'',
    }
  },
  methods: {
    clear () {
      this.error = ''
      this.message = ''
      this.invitation_url = ''
    },
    async logout () {
      await this.$axios.get(this.$config.base + '/api/logout')
    },
    async requestCredential () {
      console.log(this.first_name, this.last_name, this.email)
      this.clear()

      const { data } = await this.$axios.post(this.$config.base + '/api/credential/request', {first_name: this.first_name, last_name: this.last_name, email: this.email} )
      console.log(data)
      this.error = data?.error || ''
      this.message = data?.message || ''
      this.invitation_url = data.data?.invitation_url || ''
    }
  }
  
}
</script>
