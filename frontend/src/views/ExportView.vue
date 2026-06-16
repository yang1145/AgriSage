<template>
  <div class="export-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">数据导入导出</h1>
    </div>

    <div class="export-sections">
      <!-- Excel 汇总导出 -->
      <HudPanel title="EXCEL EXPORT / 汇总导出">
        <div class="section-content">
          <div class="form-row">
            <el-select
              v-model="excelPlotIds"
              multiple
              placeholder="选择地块..."
              class="hud-select hud-select--full"
              :disabled="exportAll"
            >
              <el-option
                v-for="p in plots"
                :key="p.id"
                :label="p.name"
                :value="p.id"
              />
            </el-select>
          </div>
          <div class="form-row">
            <el-checkbox v-model="exportAll" class="hud-checkbox">导出全部</el-checkbox>
          </div>
          <div class="form-row form-row--actions">
            <HudButton
              type="cyan"
              :disabled="excelExporting || (!exportAll && excelPlotIds.length === 0)"
              @click="handleExportExcel"
            >
              {{ excelExporting ? '正在同步本地节点...' : '导出 Excel' }}
            </HudButton>
            <span v-if="excelExporting" class="scan-anim">◆ 扫描中...</span>
          </div>
        </div>
      </HudPanel>

      <!-- PDF 档案导出 -->
      <HudPanel title="PDF EXPORT / 档案导出">
        <div class="section-content">
          <div class="form-row">
            <el-select
              v-model="pdfPlotId"
              placeholder="选择地块..."
              class="hud-select hud-select--full"
            >
              <el-option
                v-for="p in plots"
                :key="p.id"
                :label="p.name"
                :value="p.id"
              />
            </el-select>
          </div>
          <div class="form-row form-row--actions">
            <HudButton
              type="cyan"
              :disabled="pdfExporting || !pdfPlotId"
              @click="handleExportPdf"
            >
              {{ pdfExporting ? '正在生成...' : '导出 PDF' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- Excel 模板下载 -->
      <HudPanel title="EXCEL TEMPLATE / 导入模板">
        <div class="section-content">
          <div class="form-row">
            <span class="template-desc">下载标准导入模板，按格式填写后使用批量导入功能</span>
          </div>
          <div class="form-row form-row--actions">
            <HudButton type="cyan" :disabled="templateDownloading" @click="handleDownloadTemplate">
              {{ templateDownloading ? '正在下载...' : '下载模板' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- Excel 批量导入 (合作社管理员 only) -->
      <HudPanel v-if="isCoopAdmin" title="EXCEL IMPORT / 批量导入">
        <div class="section-content">
          <div class="form-row">
            <el-upload
              ref="importUploadRef"
              :auto-upload="false"
              :limit="1"
              accept=".xlsx,.xls"
              :on-change="handleImportFileChange"
              :on-remove="handleImportFileRemove"
              class="hud-upload"
            >
              <HudButton type="ghost" size="small">选择 Excel 文件</HudButton>
            </el-upload>
          </div>
          <div v-if="importResult" class="import-result">
            <div v-if="importResult.success_count" class="result-item result-item--success">
              成功导入 {{ importResult.success_count }} 条
            </div>
            <div v-if="importResult.error_count" class="result-item result-item--error">
              失败 {{ importResult.error_count }} 条
            </div>
            <div v-if="importResult.errors && importResult.errors.length" class="result-errors">
              <div v-for="(err, i) in importResult.errors" :key="i" class="result-error-line">
                行 {{ err.row }}: {{ err.message }}
              </div>
            </div>
          </div>
          <div class="form-row form-row--actions">
            <HudButton
              type="green"
              :disabled="importing || !importFile"
              @click="handleImportExcel"
            >
              {{ importing ? '正在导入...' : '导入' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- 数据库备份 (户主 only) -->
      <HudPanel v-if="isOwner" title="DATABASE BACKUP / 数据库备份">
        <div class="section-content">
          <div class="form-row form-row--actions">
            <HudButton type="cyan" :disabled="backupDownloading" @click="handleDownloadBackup">
              {{ backupDownloading ? '正在备份...' : '下载数据库备份' }}
            </HudButton>
          </div>
          <el-divider class="hud-divider" />
          <div class="form-row">
            <el-upload
              ref="restoreUploadRef"
              :auto-upload="false"
              :limit="1"
              accept=".db"
              :on-change="handleRestoreFileChange"
              :on-remove="handleRestoreFileRemove"
              class="hud-upload"
            >
              <HudButton type="ghost" size="small">选择 .db 文件</HudButton>
            </el-upload>
          </div>
          <div class="form-row">
            <div class="warning-text">
              ⚠ 恢复数据库将覆盖当前所有数据，此操作不可逆！
            </div>
          </div>
          <div class="form-row form-row--actions">
            <HudButton
              type="orange"
              :disabled="restoring || !restoreFile"
              @click="handleRestoreBackup"
            >
              {{ restoring ? '正在恢复...' : '恢复数据库' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { exportApi } from '@/api/export'
import { plotApi } from '@/api/plot'
import { useAuthStore } from '@/stores/auth'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'

const authStore = useAuthStore()

const plots = ref([])
const exportAll = ref(false)
const excelPlotIds = ref([])
const pdfPlotId = ref(null)
const importFile = ref(null)
const restoreFile = ref(null)
const importResult = ref(null)
const importUploadRef = ref(null)
const restoreUploadRef = ref(null)

const excelExporting = ref(false)
const pdfExporting = ref(false)
const importing = ref(false)
const backupDownloading = ref(false)
const restoring = ref(false)
const templateDownloading = ref(false)

const isCoopAdmin = computed(() => authStore.userRole === 'coop_admin')
const isOwner = computed(() => authStore.userRole === 'owner')

const fetchPlots = async () => {
  try {
    const res = await plotApi.getPlots()
    plots.value = res.data.plots || []
  } catch {
    ElMessage.error('获取地块列表失败')
  }
}

const downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const handleExportExcel = async () => {
  excelExporting.value = true
  try {
    const ids = exportAll.value ? [] : excelPlotIds.value
    const res = await exportApi.exportExcel(ids)
    const filename = `AgriSage_汇总_${new Date().toISOString().slice(0, 10)}.xlsx`
    downloadBlob(res.data, filename)
    ElMessage.success('Excel 导出成功')
  } catch {
    ElMessage.error('Excel 导出失败')
  } finally {
    excelExporting.value = false
  }
}

const handleExportPdf = async () => {
  if (!pdfPlotId.value) return
  pdfExporting.value = true
  try {
    const res = await exportApi.exportPdf(pdfPlotId.value)
    const plot = plots.value.find((p) => p.id === pdfPlotId.value)
    const filename = `AgriSage_${plot?.name || '地块'}_${new Date().toISOString().slice(0, 10)}.pdf`
    downloadBlob(res.data, filename)
    ElMessage.success('PDF 导出成功')
  } catch {
    ElMessage.error('PDF 导出失败')
  } finally {
    pdfExporting.value = false
  }
}

const handleImportFileChange = (file) => {
  importFile.value = file.raw
  importResult.value = null
}

const handleImportFileRemove = () => {
  importFile.value = null
  importResult.value = null
}

const handleImportExcel = async () => {
  if (!importFile.value) return
  importing.value = true
  try {
    const res = await exportApi.importExcel(importFile.value)
    importResult.value = res.data
    ElMessage.success('导入完成')
  } catch {
    ElMessage.error('导入失败')
  } finally {
    importing.value = false
  }
}

const handleDownloadBackup = async () => {
  backupDownloading.value = true
  try {
    const res = await exportApi.downloadBackup()
    const filename = `AgriSage_Backup_${new Date().toISOString().slice(0, 10)}.db`
    downloadBlob(res.data, filename)
    ElMessage.success('备份下载成功')
  } catch {
    ElMessage.error('备份下载失败')
  } finally {
    backupDownloading.value = false
  }
}

const handleRestoreFileChange = (file) => {
  restoreFile.value = file.raw
}

const handleRestoreFileRemove = () => {
  restoreFile.value = null
}

const handleRestoreBackup = async () => {
  if (!restoreFile.value) return
  try {
    await ElMessageBox.confirm(
      '恢复数据库将覆盖当前所有数据，此操作不可逆！确定要继续吗？',
      '危险操作',
      {
        confirmButtonText: '确认恢复',
        cancelButtonText: '取消',
        type: 'warning',
        customClass: 'hud-message-box',
      }
    )
  } catch {
    return
  }
  restoring.value = true
  try {
    await exportApi.restoreBackup(restoreFile.value)
    ElMessage.success('数据库恢复成功，请重新登录')
    authStore.logout()
  } catch {
    ElMessage.error('数据库恢复失败')
  } finally {
    restoring.value = false
  }
}

const handleDownloadTemplate = async () => {
  templateDownloading.value = true
  try {
    const res = await exportApi.downloadTemplate()
    const filename = `AgriSage_导入模板_${new Date().toISOString().slice(0, 10)}.xlsx`
    downloadBlob(res.data, filename)
    ElMessage.success('模板下载成功')
  } catch {
    ElMessage.error('模板下载失败')
  } finally {
    templateDownloading.value = false
  }
}

onMounted(fetchPlots)
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.export-page {
  min-height: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
}

.page-title {
  font-family: $font-mono;
  font-size: $font-size-xl;
  font-weight: 700;
  color: $accent-cyan;
  text-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
  letter-spacing: 2px;
  margin: 0;
}

.export-sections {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
  max-width: 720px;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-row {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  flex-wrap: wrap;

  &--actions {
    padding-top: $spacing-sm;
  }
}

.hud-select {
  &--full {
    width: 100%;
  }

  :deep(.el-input__wrapper) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: none;

    &:hover,
    &.is-focus {
      border-color: rgba(0, 240, 255, 0.4);
    }
  }

  :deep(.el-input__inner) {
    color: $text-primary;
    font-family: $font-mono;
    font-size: $font-size-sm;
  }

  :deep(.el-tag) {
    background: rgba(0, 240, 255, 0.1);
    border-color: rgba(0, 240, 255, 0.3);
    color: $accent-cyan;
  }
}

.hud-checkbox {
  :deep(.el-checkbox__label) {
    color: $text-secondary;
    font-family: $font-mono;
    font-size: $font-size-sm;
  }

  :deep(.el-checkbox__inner) {
    background: $bg-card;
    border-color: $border-color;
  }

  :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
    background: $accent-cyan;
    border-color: $accent-cyan;
  }
}

.scan-anim {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $accent-cyan;
  letter-spacing: 1px;
  animation: scanPulse 1.5s ease-in-out infinite;
}

@keyframes scanPulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.hud-upload {
  :deep(.el-upload-list) {
    .el-upload-list__item {
      background: $bg-card;
      border-color: $border-color;
      color: $text-primary;
      font-family: $font-mono;
      font-size: $font-size-xs;
    }
  }
}

.import-result {
  padding: $spacing-sm;
  border: 1px solid $border-color;
  border-radius: $radius-sm;
  background: rgba(0, 240, 255, 0.03);
}

.result-item {
  font-family: $font-mono;
  font-size: $font-size-sm;
  margin-bottom: $spacing-xs;

  &--success {
    color: $accent-green;
  }

  &--error {
    color: $status-error;
  }
}

.result-errors {
  max-height: 120px;
  overflow-y: auto;
}

.result-error-line {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $accent-orange;
  line-height: 1.6;
}

.hud-divider {
  border-color: $border-color;
}

.warning-text {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $accent-orange;
  letter-spacing: 1px;
  line-height: 1.5;
}

.template-desc {
  font-family: $font-mono;
  font-size: $font-size-sm;
  color: $text-secondary;
  line-height: 1.5;
}
</style>
