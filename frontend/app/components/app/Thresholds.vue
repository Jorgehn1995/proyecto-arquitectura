<template>
  <v-container fluid>
    <!-- Header con título -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <div>
            <h1 class="text-h4 font-weight-bold">Configuración de Umbrales</h1>
            <p class="text-subtitle-1 text-medium-emphasis">
              Configura los límites de temperatura y humedad del sistema
            </p>
          </div>
          <v-btn
            v-if="!threshold"
            color="primary"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateDialog"
          >
            Configurar Umbrales
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Card de configuración actual -->
    <v-row v-if="threshold && !loading">
      <v-col cols="12" md="6">
        <!-- Humedad -->
        <v-card elevation="2" class="mb-4">
          <v-card-title >
            <v-icon class="mr-2" color="blue">mdi-water</v-icon>
            Umbrales de Humedad
          </v-card-title>
          <v-card-text class="pa-6">
            <div class="d-flex justify-space-around align-center">
              <div class="text-center">
                <v-icon size="48" color="blue-lighten-2">mdi-water-minus</v-icon>
                <div class="text-h4 font-weight-bold mt-2">{{ threshold.min_humidity }}%</div>
                <div class="text-caption text-medium-emphasis">Mínimo</div>
              </div>
              <v-icon size="32" color="grey-lighten-1">mdi-arrow-left-right</v-icon>
              <div class="text-center">
                <v-icon size="48" color="blue-darken-2">mdi-water-plus</v-icon>
                <div class="text-h4 font-weight-bold mt-2">{{ threshold.max_humidity }}%</div>
                <div class="text-caption text-medium-emphasis">Máximo</div>
              </div>
            </div>
            
            <v-divider class="my-4" />
            
            <div class="d-flex align-center">
              <v-icon size="small" class="mr-2">mdi-information</v-icon>
              <span class="text-caption">
                Rango válido: {{ threshold.min_humidity }}% - {{ threshold.max_humidity }}%
              </span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <!-- Temperatura -->
        <v-card elevation="2" class="mb-4">
          <v-card-title >
            <v-icon class="mr-2" color="red">mdi-thermometer</v-icon>
            Umbrales de Temperatura
          </v-card-title>
          <v-card-text class="pa-6">
            <div class="d-flex justify-space-around align-center">
              <div class="text-center">
                <v-icon size="48" color="blue">mdi-thermometer-low</v-icon>
                <div class="text-h4 font-weight-bold mt-2">{{ threshold.min_temperature }}°C</div>
                <div class="text-caption text-medium-emphasis">Mínimo</div>
              </div>
              <v-icon size="32" color="grey-lighten-1">mdi-arrow-left-right</v-icon>
              <div class="text-center">
                <v-icon size="48" color="red">mdi-thermometer-high</v-icon>
                <div class="text-h4 font-weight-bold mt-2">{{ threshold.max_temperature }}°C</div>
                <div class="text-caption text-medium-emphasis">Máximo</div>
              </div>
            </div>
            
            <v-divider class="my-4" />
            
            <div class="d-flex align-center">
              <v-icon size="small" class="mr-2">mdi-information</v-icon>
              <span class="text-caption">
                Rango válido: {{ threshold.min_temperature }}°C - {{ threshold.max_temperature }}°C
              </span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Información adicional -->
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-calendar-clock</v-icon>
            Información del Registro
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2">mdi-calendar-plus</v-icon>
                  <span class="text-caption text-medium-emphasis">Creado:</span>
                  <span class="text-caption font-weight-medium ml-2">
                    {{ formatDate(threshold.created_at) }}
                  </span>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2">mdi-calendar-edit</v-icon>
                  <span class="text-caption text-medium-emphasis">Última actualización:</span>
                  <span class="text-caption font-weight-medium ml-2">
                    {{ formatDate(threshold.updated_at) }}
                  </span>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="px-4 pb-4">
            <v-spacer />
            <v-btn
              color="primary"
              prepend-icon="mdi-pencil"
              @click="openEditDialog"
            >
              Editar Umbrales
            </v-btn>
            <v-btn
              color="error"
              variant="outlined"
              prepend-icon="mdi-delete"
              @click="confirmDelete"
            >
              Eliminar Configuración
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Validador de lecturas -->
      <v-col cols="12">
        <v-card elevation="2" color="primary" variant="tonal">
          <v-card-title>
            <v-icon class="mr-2">mdi-check-circle</v-icon>
            Validador de Lecturas
          </v-card-title>
          <v-card-text>
            <p class="mb-4">
              Prueba si los valores de humedad y temperatura están dentro de los umbrales configurados
            </p>
            <v-row>
              <v-col cols="12" md="5">
                <v-text-field
                  v-model.number="validatorData.humidity"
                  label="Humedad (%)"
                  prepend-inner-icon="mdi-water"
                  type="number"
                  suffix="%"
                  :rules="[rules.humidity]"
                />
              </v-col>
              <v-col cols="12" md="5">
                <v-text-field
                  v-model.number="validatorData.temperature"
                  label="Temperatura (°C)"
                  prepend-inner-icon="mdi-thermometer"
                  type="number"
                  suffix="°C"
                />
              </v-col>
              <v-col cols="12" md="2" class="d-flex align-center">
                <v-btn
                  color="primary"
                  block
                  @click="validateReadings"
                  :loading="validating"
                >
                  Validar
                </v-btn>
              </v-col>
            </v-row>

            <!-- Resultado de validación -->
            <v-alert
              v-if="validationResult"
              :type="validationResult.status === 'ok' ? 'success' : 'error'"
              variant="tonal"
              class="mt-4"
              :icon="validationResult.status === 'ok' ? 'mdi-check-circle' : 'mdi-alert-circle'"
            >
              <div class="font-weight-medium mb-2">{{ validationResult.message }}</div>
              <ul v-if="validationResult.errors && validationResult.errors.length > 0" class="ml-4">
                <li v-for="(error, index) in validationResult.errors" :key="index" class="text-caption">
                  {{ error }}
                </li>
              </ul>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Estado de carga -->
    <v-row v-if="loading">
      <v-col cols="12" md="6">
        <v-skeleton-loader type="card" />
      </v-col>
      <v-col cols="12" md="6">
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>

    <!-- Sin configuración -->
    <v-row v-if="!threshold && !loading">
      <v-col cols="12">
        <v-card elevation="2" class="text-center pa-8">
          <v-icon size="80" color="grey-lighten-1">mdi-thermometer-alert</v-icon>
          <h2 class="text-h5 mt-4 mb-2">No hay umbrales configurados</h2>
          <p class="text-body-2 text-medium-emphasis mb-4">
            Configura los límites de temperatura y humedad para el sistema de monitoreo
          </p>
          <v-btn color="primary" size="large" @click="openCreateDialog">
            Configurar Ahora
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog para Crear/Editar Umbrales -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5 text-white">
            {{ isEditing ? 'Editar Umbrales' : 'Configurar Umbrales' }}
          </span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-form ref="formRef" v-model="formValid">
            <!-- Humedad -->
            <div class="mb-4">
              <h3 class="text-h6 mb-3">
                <v-icon class="mr-2" color="blue">mdi-water</v-icon>
                Umbrales de Humedad
              </h3>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.min_humidity"
                    label="Humedad Mínima *"
                    prepend-inner-icon="mdi-water-minus"
                    type="number"
                    suffix="%"
                    :rules="[rules.required, rules.humidity]"
                    :error-messages="errors.min_humidity"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.max_humidity"
                    label="Humedad Máxima *"
                    prepend-inner-icon="mdi-water-plus"
                    type="number"
                    suffix="%"
                    :rules="[rules.required, rules.humidity]"
                    :error-messages="errors.max_humidity"
                  />
                </v-col>
              </v-row>
            </div>

            <v-divider class="my-4" />

            <!-- Temperatura -->
            <div class="mb-4">
              <h3 class="text-h6 mb-3">
                <v-icon class="mr-2" color="red">mdi-thermometer</v-icon>
                Umbrales de Temperatura
              </h3>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.min_temperature"
                    label="Temperatura Mínima *"
                    prepend-inner-icon="mdi-thermometer-low"
                    type="number"
                    suffix="°C"
                    :rules="[rules.required]"
                    :error-messages="errors.min_temperature"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="formData.max_temperature"
                    label="Temperatura Máxima *"
                    prepend-inner-icon="mdi-thermometer-high"
                    type="number"
                    suffix="°C"
                    :rules="[rules.required]"
                    :error-messages="errors.max_temperature"
                  />
                </v-col>
              </v-row>
            </div>

            <v-alert type="info" variant="tonal" class="mt-4">
              <div class="text-caption">
                <strong>Nota:</strong> El mínimo debe ser menor que el máximo en ambos casos.
              </div>
            </v-alert>
          </v-form>

          <v-alert
            v-if="formError"
            type="error"
            variant="tonal"
            class="mt-4"
            closable
            @click:close="formError = ''"
          >
            {{ formError }}
          </v-alert>
        </v-card-text>

        <v-card-actions class="px-6 pb-6">
          <v-spacer />
          <v-btn
            variant="text"
            @click="closeDialog"
            :disabled="saving"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            variant="elevated"
            @click="saveThreshold"
            :loading="saving"
            :disabled="!formValid"
          >
            {{ isEditing ? 'Actualizar' : 'Guardar' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de Confirmación de Eliminación -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5 text-white">Confirmar Eliminación</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-alert type="warning" variant="tonal" class="mb-4">
            Esta acción eliminará toda la configuración de umbrales
          </v-alert>
          
          <p class="text-body-1">
            ¿Está seguro que desea eliminar la configuración de umbrales?
          </p>
          
          <div v-if="threshold" class="mt-4 pa-3 rounded ">
            <div class="mb-2">
              <strong>Humedad:</strong> {{ threshold.min_humidity }}% - {{ threshold.max_humidity }}%
            </div>
            <div>
              <strong>Temperatura:</strong> {{ threshold.min_temperature }}°C - {{ threshold.max_temperature }}°C
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="px-6 pb-6">
          <v-spacer />
          <v-btn
            variant="text"
            @click="deleteDialog = false"
            :disabled="deleting"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            variant="elevated"
            @click="deleteThresholdConfirmed"
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificaciones -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top right"
    >
      {{ snackbar.message }}
      <template #actions>
        <v-btn
          icon="mdi-close"
          size="small"
          @click="snackbar.show = false"
        />
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/base/useApi';

const api = useApi();

// ============================================
// INTERFACES
// ============================================

interface Threshold {
  id: number;
  min_humidity: number;
  max_humidity: number;
  min_temperature: number;
  max_temperature: number;
  created_at: string;
  updated_at: string;
}

interface ValidationResult {
  status: string;
  message: string;
  humidity: number;
  temperature: number;
  errors?: string[];
  thresholds?: {
    min_humidity: number;
    max_humidity: number;
    min_temperature: number;
    max_temperature: number;
  };
}

// ============================================
// STATE
// ============================================

const threshold = ref<Threshold | null>(null);
const loading = ref(false);

// Dialog states
const dialog = ref(false);
const deleteDialog = ref(false);

// Form states
const formRef = ref();
const formValid = ref(false);
const formData = ref({
  min_humidity: 30,
  max_humidity: 70,
  min_temperature: 18,
  max_temperature: 28,
});
const errors = ref({
  min_humidity: '',
  max_humidity: '',
  min_temperature: '',
  max_temperature: '',
});
const formError = ref('');
const isEditing = ref(false);
const saving = ref(false);

// Delete states
const deleting = ref(false);

// Validator states
const validatorData = ref({
  humidity: 50,
  temperature: 22,
});
const validationResult = ref<ValidationResult | null>(null);
const validating = ref(false);

// Snackbar
const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
});

// ============================================
// VALIDATION RULES
// ============================================

const rules = {
  required: (v: any) => (v !== null && v !== undefined && v !== '') || 'Este campo es requerido',
  humidity: (v: number) => {
    if (v === null || v === undefined) return 'Este campo es requerido';
    return (v >= 0 && v <= 100) || 'Debe estar entre 0 y 100';
  },
};

// ============================================
// METHODS
// ============================================

const loadThreshold = async () => {
  loading.value = true;
  try {
    threshold.value = await api.get<Threshold>('/thresholds');
  } catch (error: any) {
    // Si no existe configuración (404), no mostramos error
    if (!error.message?.includes('404')) {
      console.error('Error loading threshold:', error);
    }
    threshold.value = null;
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  isEditing.value = false;
  formData.value = {
    min_humidity: 30,
    max_humidity: 70,
    min_temperature: 18,
    max_temperature: 28,
  };
  errors.value = {
    min_humidity: '',
    max_humidity: '',
    min_temperature: '',
    max_temperature: '',
  };
  formError.value = '';
  dialog.value = true;
};

const openEditDialog = () => {
  if (!threshold.value) return;
  
  isEditing.value = true;
  formData.value = {
    min_humidity: threshold.value.min_humidity,
    max_humidity: threshold.value.max_humidity,
    min_temperature: threshold.value.min_temperature,
    max_temperature: threshold.value.max_temperature,
  };
  errors.value = {
    min_humidity: '',
    max_humidity: '',
    min_temperature: '',
    max_temperature: '',
  };
  formError.value = '';
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  formRef.value?.reset();
};

const saveThreshold = async () => {
  if (!formValid.value) return;

  // Validar que min < max
  if (formData.value.min_humidity >= formData.value.max_humidity) {
    formError.value = 'La humedad mínima debe ser menor que la máxima';
    return;
  }
  if (formData.value.min_temperature >= formData.value.max_temperature) {
    formError.value = 'La temperatura mínima debe ser menor que la máxima';
    return;
  }

  saving.value = true;
  errors.value = {
    min_humidity: '',
    max_humidity: '',
    min_temperature: '',
    max_temperature: '',
  };
  formError.value = '';

  try {
    const thresholdData = {
      min_humidity: formData.value.min_humidity,
      max_humidity: formData.value.max_humidity,
      min_temperature: formData.value.min_temperature,
      max_temperature: formData.value.max_temperature,
    };

    if (isEditing.value && threshold.value) {
      await api.put<Threshold>(`/thresholds/${threshold.value.id}`, thresholdData);
      showSnackbar('Umbrales actualizados correctamente', 'success');
    } else {
      await api.post<Threshold>('/thresholds', thresholdData);
      showSnackbar('Umbrales configurados correctamente', 'success');
    }

    closeDialog();
    await loadThreshold();
  } catch (error: any) {
    const errorMessage = error.message || 'Error al guardar umbrales';
    formError.value = errorMessage;
    showSnackbar(errorMessage, 'error');
  } finally {
    saving.value = false;
  }
};

const confirmDelete = () => {
  deleteDialog.value = true;
};

const deleteThresholdConfirmed = async () => {
  if (!threshold.value) return;

  deleting.value = true;
  try {
    await api.delete(`/thresholds/${threshold.value.id}`);
    showSnackbar('Configuración eliminada correctamente', 'success');
    deleteDialog.value = false;
    threshold.value = null;
  } catch (error) {
    showSnackbar('Error al eliminar configuración', 'error');
    console.error('Error deleting threshold:', error);
  } finally {
    deleting.value = false;
  }
};

const validateReadings = async () => {
  if (validatorData.value.humidity === null || validatorData.value.temperature === null) {
    showSnackbar('Ingrese valores de humedad y temperatura', 'warning');
    return;
  }

  validating.value = true;
  validationResult.value = null;

  try {
    const result = await api.post<ValidationResult>('/thresholds/validate', {
      humidity: validatorData.value.humidity,
      temperature: validatorData.value.temperature,
    });
    validationResult.value = result;
    
    if (result.status === 'ok') {
      showSnackbar('Lecturas dentro de los umbrales', 'success');
    } else {
      showSnackbar('Lecturas fuera de los umbrales', 'warning');
    }
  } catch (error: any) {
    // El error 400 contiene la respuesta con los errores
    if (error.message) {
      try {
        // Intentar parsear el mensaje de error como JSON
        const errorData = JSON.parse(error.message);
        validationResult.value = errorData;
      } catch {
        showSnackbar('Error al validar lecturas', 'error');
      }
    } else {
      showSnackbar('Error al validar lecturas', 'error');
    }
  } finally {
    validating.value = false;
  }
};

const showSnackbar = (message: string, color: string = 'success') => {
  snackbar.value = {
    show: true,
    message,
    color,
  };
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadThreshold();
});
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}
</style>
