<template>
  <el-row>
    <el-form :model="search" :inline="true" ref="searchRef">
      <el-form-item label="用户名" prop="name">
        <el-input v-model="search.name"/>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="search.email"/>
      </el-form-item>
      <el-form-item label="状态" prop="enable">
        <div style="width: 100px">
          <auto-dict dict-type="select" code="enable_code" v-model="search.enable"/>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
        <el-button type="primary" @click="handleReset" :icon="RefreshRight">重置</el-button>
        <el-button v-permission="'user:add'" type="primary" @click="handleAdd" :icon="Plus">添加新用户</el-button>
      </el-form-item>
    </el-form>
  </el-row>

  <div style="padding-top:10px">
    <el-table :data="tableData" border style="width: 100%" stripe
              :header-cell-style="{background:'#eef1f6',color:'#606266'}">
      <el-table-column label="#" type="index" width="50"/>
      <el-table-column prop="name" label="用户名" align="center"/>
      <el-table-column prop="email" label="邮箱" align="center"/>
      <el-table-column prop="avatar" label="头像" align="center"/>
      <el-table-column label="状态" align="center">
        <template #default="scope">
          <el-tag effect="dark" :type="scope.row.enable === true?'success':'danger'">
            {{ scope.row.enable === true ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template #default="scope">
          <el-button style="padding: 0;" text type="primary" @click="handleEdit(scope.row.id)" :icon="Edit">编辑
          </el-button>
          <el-divider direction="vertical"/>
          <el-button style="padding: 0;" text type="primary" @click="handleChangePwd(scope.row)" :icon="Unlock">
            重置密码
          </el-button>
          <el-divider direction="vertical"/>
          <el-button style="padding: 0;" text type="danger" @click="handleDel(scope.row)" :icon="Delete">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total" background
                   layout="total,prev,pager,next,sizes,jumper"
                   style="margin-top: 10px;"
    />

  </div>

  <ResetPasswdDialog ref="resetPasswdDialogRef"/>
  <user-drawer ref="userDrawerRef" @success="freshCurrentPage"/>

</template>

<script setup>
  defineOptions({
    name: '用户管理'
  })

  import {
    reactive,
    ref, watch, onMounted
  } from 'vue'
  import {
    Edit, Delete, Unlock,
    Search, RefreshRight, Plus
  } from '@element-plus/icons-vue'
  import UserDrawer from './UserDrawer.vue'
  import ResetPasswdDialog from './ResetPasswdDialog.vue'
  import usePagination from '@/composables/usePagination'
  import {
    DeleteUser, GetUserInfo
  } from '@/api/users'
  import {ElMessage, ElMessageBox} from 'element-plus'
  import AutoDict from '@/components/AutoDict'

  const detailVisible = ref(false)
  const resetPasswdDialogRef = ref(null)
  const selectUser = reactive({})
  const searchRef = ref(null)
  const userDrawerRef = ref(null)

  const searchForm = {
    name: null,
    email: null,
    enable: null
  }

  // 首次打开页面先进行初始化

  const {
    search,
    tableData,
    currentPage,
    pageSize,
    orderModel,
    total,
    freshCurrentPage,
    handleSearch
  } = usePagination('/api/users/search', searchForm)

  function handleReset() {
    searchRef.value.resetFields()
    handleSearch()
  }

  function handleChangePwd(user) {
    resetPasswdDialogRef.value.reset(user)
  }


  async function handleEdit(uid) {
    await userDrawerRef.value.edit(uid)
  }

  async function handleAdd() {
    console.log('start to add user')
    await userDrawerRef.value.add()
  }


  function handleDel(userInfo) {
    if (userInfo.name === 'admin') {
      ElMessage({
        message: 'admin用户无法删除',
        type: 'warning'
      })
      return false
    }
    ElMessageBox.confirm('是否确定要删除用户：' + userInfo.name, '警告', {type: 'warning'}).then(() => {
      DeleteUser(userInfo.id).then(() => {
        ElMessage({
          title: 'success',
          message: userInfo.name + '用户删除成功',
          type: 'success'
        })
        freshCurrentPage()
      })
    }).catch(() => {
      ElMessage({
        title: 'success',
        message: '取消删除操作',
        type: 'warning'
      })
    })
  }

  watch(
      detailVisible, (newValue, oldValue) => {
        if (newValue === false) {
          freshCurrentPage()
        }
      })

  onMounted(() => {
    handleSearch()
  })
</script>

<style>
</style>
