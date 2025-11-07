<template>
  <v-container fluid>
    <!-- Header con título y botón para agregar -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <div>
            <h1 class="text-h4 font-weight-bold">Gestión de Lecturas</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Administra las lecturas de sensores del sistema</p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateDialog"
          >
            Nueva Lectura
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Barra de búsqueda y filtros -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Buscar lecturas..."
          density="comfortable"
          clearable
          hide-details
        />
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center justify-end">
        <v-chip
          class="mr-2"
          prepend-icon="mdi-chart-line"
          color="primary"
          variant="tonal"
        >
          Total: {{ reads.length }}
        </v-chip>
        <v-btn
          icon="mdi-refresh"
          variant="text"
          @click="loadReads"
          :loading="loading"
        />
      </v-col>
    </v-row>

    <!-- Tabla de lecturas -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredReads"
        :loading="loading"
        :search="search"
        item-value="id"
        class="elevation-0"
      >
        <!-- Loading -->
        <template #loading>
          <v-skeleton-loader type="table-row@5" />
        </template>

        <!-- Column: Nombre -->
        <template #item.name="{ item }">
          <div class="d-flex align-center py-2">
            <v-icon class="mr-3" color="primary">mdi-file-document</v-icon>
            <div>
              <div class="font-weight-medium">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">ID: #{{ item.id }}</div>
            </div>
          </div>
        </template>

        <!-- Column: Usuario -->
        <template #item.user_id="{ item }">
          <v-chip
            v-if="item.user_id"
            size="small"
            color="info"
            variant="tonal"
            prepend-icon="mdi-account"
          >
            Usuario #{{ item.user_id }}
          </v-chip>
          <span v-else class="text-medium-emphasis text-caption">Sin usuario</span>
        </template>

        <!-- Column: Sensor -->
        <template #item.sensor="{ item }">
          <div v-if="item.sensor" class="text-caption">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" class="mr-1" color="blue">mdi-water</v-icon>
              <strong>{{ item.sensor.humidity }}%</strong>
            </div>
            <div class="d-flex align-center">
              <v-icon size="small" class="mr-1" color="red">mdi-thermometer</v-icon>
              <strong>{{ item.sensor.temperature }}°C</strong>
            </div>
          </div>
          <span v-else class="text-medium-emphasis text-caption">Sin sensor</span>
        </template>

        <!-- Column: Bomba -->
        <template #item.pump="{ item }">
          <v-chip
            v-if="item.pump"
            size="small"
            :color="item.pump.status ? 'success' : 'error'"
            variant="tonal"
          >
            <v-icon start :icon="item.pump.status ? 'mdi-pump' : 'mdi-pump-off'" />
            {{ item.pump.status ? 'ON' : 'OFF' }}
          </v-chip>
          <span v-else class="text-medium-emphasis text-caption">Sin bomba</span>
        </template>

        <!-- Column: Ventilador -->
        <template #item.fan="{ item }">
          <v-chip
            v-if="item.fan"
            size="small"
            :color="item.fan.status ? 'success' : 'error'"
            variant="tonal"
          >
            <v-icon start :icon="item.fan.status ? 'mdi-fan' : 'mdi-fan-off'" />
            {{ item.fan.status ? 'ON' : 'OFF' }}
          </v-chip>
          <span v-else class="text-medium-emphasis text-caption">Sin ventilador</span>
        </template>

        <!-- Column: Humo -->
        <template #item.smoke="{ item }">
          <v-chip
            v-if="item.smoke"
            size="small"
            :color="item.smoke.status ? 'error' : 'success'"
            variant="tonal"
          >
            <v-icon start :icon="item.smoke.status ? 'mdi-smoke-detector-alert' : 'mdi-smoke-detector'" />
            {{ item.smoke.status ? 'DETECTADO' : 'NORMAL' }}
          </v-chip>
          <span v-else class="text-medium-emphasis text-caption">Sin detector</span>
        </template>

        <!-- Column: Timestamp -->
        <template #item.timestamp="{ item }">
          <div class="text-caption">
            {{ formatDate(item.timestamp) }}
          </div>
        </template>

        <!-- Column: Acciones -->
        <template #item.actions="{ item }">
          <div class="d-flex gap-1">
            <v-tooltip text="Ver detalles" location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewRead(item)"
                />
              </template>
            </v-tooltip>
            <v-tooltip text="Editar" location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="editRead(item)"
                />
              </template>
            </v-tooltip>
            <v-tooltip text="Eliminar" location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                />
              </template>
            </v-tooltip>
          </div>
        </template>

        <!-- No data -->
        <template #no-data>
          <div class="text-center py-8">
            <v-icon size="64" color="grey-lighten-1">mdi-chart-line-variant</v-icon>
            <p class="text-h6 text-medium-emphasis mt-4">No hay lecturas registradas</p>
            <v-btn color="primary" class="mt-2" @click="openCreateDialog">
              Crear primera lectura
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Dialog para Crear/Editar Lectura -->
    <v-dialog v-model="dialog" max-width="800px" persistent scrollable>
      <v-card>
        <v-card-title>
          <span class="text-h5 text-white">
            {{ isEditing ? 'Editar Lectura' : 'Nueva Lectura' }}
          </span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-form ref="formRef" v-model="formValid">
            <!-- Información General -->
            <div class="mb-4">
              <h3 class="text-h6 mb-3">
                <v-icon class="mr-2">mdi-information</v-icon>
                Información General
              </h3>
              <v-row>
                <v-col cols="12" md="8">
                  <v-text-field
                    v-model="formData.name"
                    label="Nombre de la lectura *"
                    prepend-inner-icon="mdi-file-document"
                    :rules="[rules.required, rules.minLength(2)]"
                    :error-messages="errors.name"
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model.number="formData.user_id"
                    label="ID Usuario (opcional)"
                    prepend-inner-icon="mdi-account"
                    type="number"
                    :error-messages="errors.user_id"
                  />
                </v-col>
              </v-row>
            </div>

            <v-divider class="my-4" />

            <!-- Sensor -->
            <div class="mb-4">
              <div class="d-flex align-center mb-3">
                <h3 class="text-h6">
                  <v-icon class="mr-2" color="blue">mdi-thermometer-lines</v-icon>
                  Sensor DHT
                </h3>
                <v-spacer />
                <v-switch
                  v-model="formData.includeSensor"
                  color="primary"
                  hide-details
                  density="compact"
                  label="Incluir sensor"
                />
              </div>
              
              <v-expand-transition>
                <v-row v-if="formData.includeSensor">
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model.number="formData.sensor.humidity"
                      label="Humedad (%) *"
                      prepend-inner-icon="mdi-water"
                      type="number"
                      suffix="%"
                      :rules="formData.includeSensor ? [rules.required, rules.humidity] : []"
                      :error-messages="errors.sensor?.humidity"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model.number="formData.sensor.temperature"
                      label="Temperatura (°C) *"
                      prepend-inner-icon="mdi-thermometer"
                      type="number"
                      suffix="°C"
                      :rules="formData.includeSensor ? [rules.required] : []"
                      :error-messages="errors.sensor?.temperature"
                    />
                  </v-col>
                </v-row>
              </v-expand-transition>
            </div>

            <v-divider class="my-4" />

            <!-- Bomba -->
            <div class="mb-4">
              <div class="d-flex align-center mb-3">
                <h3 class="text-h6">
                  <v-icon class="mr-2" color="purple">mdi-pump</v-icon>
                  Bomba
                </h3>
                <v-spacer />
                <v-switch
                  v-model="formData.includePump"
                  color="primary"
                  hide-details
                  density="compact"
                  label="Incluir bomba"
                />
              </div>
              
              <v-expand-transition>
                <v-row v-if="formData.includePump">
                  <v-col cols="12">
                    <v-switch
                      v-model="formData.pump.status"
                      color="success"
                      label="Estado de la bomba"
                      :true-value="true"
                      :false-value="false"
                      hide-details
                    >
                      <template #prepend>
                        <v-icon :color="formData.pump.status ? 'success' : 'error'">
                          {{ formData.pump.status ? 'mdi-pump' : 'mdi-pump-off' }}
                        </v-icon>
                      </template>
                    </v-switch>
                  </v-col>
                </v-row>
              </v-expand-transition>
            </div>

            <v-divider class="my-4" />

            <!-- Ventilador -->
            <div class="mb-4">
              <div class="d-flex align-center mb-3">
                <h3 class="text-h6">
                  <v-icon class="mr-2" color="teal">mdi-fan</v-icon>
                  Ventilador
                </h3>
                <v-spacer />
                <v-switch
                  v-model="formData.includeFan"
                  color="primary"
                  hide-details
                  density="compact"
                  label="Incluir ventilador"
                />
              </div>
              
              <v-expand-transition>
                <v-row v-if="formData.includeFan">
                  <v-col cols="12">
                    <v-switch
                      v-model="formData.fan.status"
                      color="success"
                      label="Estado del ventilador"
                      :true-value="true"
                      :false-value="false"
                      hide-details
                    >
                      <template #prepend>
                        <v-icon :color="formData.fan.status ? 'success' : 'error'">
                          {{ formData.fan.status ? 'mdi-fan' : 'mdi-fan-off' }}
                        </v-icon>
                      </template>
                    </v-switch>
                  </v-col>
                </v-row>
              </v-expand-transition>
            </div>

            <v-divider class="my-4" />

            <!-- Detector de Humo -->
            <div class="mb-4">
              <div class="d-flex align-center mb-3">
                <h3 class="text-h6">
                  <v-icon class="mr-2" color="orange">mdi-smoke-detector</v-icon>
                  Detector de Humo
                </h3>
                <v-spacer />
                <v-switch
                  v-model="formData.includeSmoke"
                  color="primary"
                  hide-details
                  density="compact"
                  label="Incluir detector"
                />
              </div>
              
              <v-expand-transition>
                <v-row v-if="formData.includeSmoke">
                  <v-col cols="12">
                    <v-switch
                      v-model="formData.smoke.status"
                      color="error"
                      label="Estado del detector"
                      :true-value="true"
                      :false-value="false"
                      hide-details
                    >
                      <template #prepend>
                        <v-icon :color="formData.smoke.status ? 'error' : 'success'">
                          {{ formData.smoke.status ? 'mdi-smoke-detector-alert' : 'mdi-smoke-detector' }}
                        </v-icon>
                      </template>
                    </v-switch>
                  </v-col>
                </v-row>
              </v-expand-transition>
            </div>
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
            @click="saveRead"
            :loading="saving"
            :disabled="!formValid"
          >
            {{ isEditing ? 'Actualizar' : 'Crear' }}
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
            Esta acción no se puede deshacer y eliminará todas las entidades relacionadas
          </v-alert>
          
          <p class="text-body-1">
            ¿Está seguro que desea eliminar la lectura 
            <strong>{{ readToDelete?.name }}</strong>?
          </p>
          
          <div v-if="readToDelete" class="mt-4 pa-3 rounded">
            <div class="d-flex align-center mb-2">
              <v-icon size="small" class="mr-2">mdi-identifier</v-icon>
              <span class="text-caption">ID: #{{ readToDelete.id }}</span>
            </div>
            <div class="d-flex align-center">
              <v-icon size="small" class="mr-2">mdi-calendar</v-icon>
              <span class="text-caption">{{ formatDate(readToDelete.timestamp) }}</span>
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
            @click="deleteReadConfirmed"
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de Detalles de la Lectura -->
    <v-dialog v-model="viewDialog" max-width="700px" scrollable>
      <v-card v-if="selectedRead">
        <v-card-title>
          <span class="text-h5 text-white">Detalles de la Lectura</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <div class="text-center mb-6">
            <v-icon size="64" color="primary">mdi-file-chart</v-icon>
            <h2 class="text-h5 mt-3">{{ selectedRead.name }}</h2>
            <p class="text-caption text-medium-emphasis">ID: #{{ selectedRead.id }}</p>
          </div>

          <!-- Información General -->
          <v-card variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1 bg-surface-variant">
              <v-icon class="mr-2">mdi-information</v-icon>
              Información General
            </v-card-title>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-calendar</v-icon>
                </template>
                <v-list-item-title>Timestamp</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(selectedRead.timestamp) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-account</v-icon>
                </template>
                <v-list-item-title>Usuario</v-list-item-title>
                <v-list-item-subtitle>
                  {{ selectedRead.user_id ? `Usuario #${selectedRead.user_id}` : 'No asignado' }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Sensor -->
          <v-card v-if="selectedRead.sensor" variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1 bg-surface-variant">
              <v-icon class="mr-2" color="blue">mdi-thermometer-lines</v-icon>
              Sensor DHT
            </v-card-title>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon color="blue">mdi-water</v-icon>
                </template>
                <v-list-item-title>Humedad</v-list-item-title>
                <v-list-item-subtitle>{{ selectedRead.sensor.humidity }}%</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template #prepend>
                  <v-icon color="red">mdi-thermometer</v-icon>
                </template>
                <v-list-item-title>Temperatura</v-list-item-title>
                <v-list-item-subtitle>{{ selectedRead.sensor.temperature }}°C</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Bomba -->
          <v-card v-if="selectedRead.pump" variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1 bg-surface-variant">
              <v-icon class="mr-2" color="purple">mdi-pump</v-icon>
              Bomba
            </v-card-title>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon :color="selectedRead.pump.status ? 'success' : 'error'">
                    {{ selectedRead.pump.status ? 'mdi-pump' : 'mdi-pump-off' }}
                  </v-icon>
                </template>
                <v-list-item-title>Estado</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip
                    size="small"
                    :color="selectedRead.pump.status ? 'success' : 'error'"
                    variant="tonal"
                  >
                    {{ selectedRead.pump.status ? 'Encendida' : 'Apagada' }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Ventilador -->
          <v-card v-if="selectedRead.fan" variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1 bg-surface-variant">
              <v-icon class="mr-2" color="teal">mdi-fan</v-icon>
              Ventilador
            </v-card-title>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon :color="selectedRead.fan.status ? 'success' : 'error'">
                    {{ selectedRead.fan.status ? 'mdi-fan' : 'mdi-fan-off' }}
                  </v-icon>
                </template>
                <v-list-item-title>Estado</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip
                    size="small"
                    :color="selectedRead.fan.status ? 'success' : 'error'"
                    variant="tonal"
                  >
                    {{ selectedRead.fan.status ? 'Encendido' : 'Apagado' }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Detector de Humo -->
          <v-card v-if="selectedRead.smoke" variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1 bg-surface-variant">
              <v-icon class="mr-2" color="orange">mdi-smoke-detector</v-icon>
              Detector de Humo
            </v-card-title>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon :color="selectedRead.smoke.status ? 'error' : 'success'">
                    {{ selectedRead.smoke.status ? 'mdi-smoke-detector-alert' : 'mdi-smoke-detector' }}
                  </v-icon>
                </template>
                <v-list-item-title>Estado</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip
                    size="small"
                    :color="selectedRead.smoke.status ? 'error' : 'success'"
                    variant="tonal"
                  >
                    {{ selectedRead.smoke.status ? 'Humo Detectado' : 'Normal' }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-card-text>

        <v-card-actions class="px-6 pb-6">
          <v-spacer />
          <v-btn
            color="primary"
            variant="text"
            @click="editRead(selectedRead)"
          >
            Editar
          </v-btn>
          <v-btn
            variant="elevated"
            @click="viewDialog = false"
          >
            Cerrar
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
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/base/useApi';

const api = useApi();

// ============================================
// INTERFACES
// ============================================

interface Sensor {
  id?: number;
  read_id?: number;
  humidity: number;
  temperature: number;
}

interface Pump {
  id?: number;
  read_id?: number;
  status: boolean;
}

interface Fan {
  id?: number;
  read_id?: number;
  status: boolean;
}

interface Smoke {
  id?: number;
  read_id?: number;
  status: boolean;
}

interface Read {
  id: number;
  name: string;
  user_id?: number | null;
  timestamp: string;
  created_at: string;
  sensor?: Sensor | null;
  pump?: Pump | null;
  fan?: Fan | null;
  smoke?: Smoke | null;
}

// ============================================
// STATE
// ============================================

const reads = ref<Read[]>([]);
const loading = ref(false);
const search = ref('');

// Dialog states
const dialog = ref(false);
const deleteDialog = ref(false);
const viewDialog = ref(false);

// Form states
const formRef = ref();
const formValid = ref(false);
const formData = ref({
  name: '',
  user_id: null as number | null,
  includeSensor: false,
  sensor: {
    humidity: 0,
    temperature: 0,
  },
  includePump: false,
  pump: {
    status: false,
  },
  includeFan: false,
  fan: {
    status: false,
  },
  includeSmoke: false,
  smoke: {
    status: false,
  },
});
const errors = ref({
  name: '',
  user_id: '',
  sensor: {
    humidity: '',
    temperature: '',
  },
  pump: {},
  fan: {},
  smoke: {},
});
const formError = ref('');
const isEditing = ref(false);
const editingReadId = ref<number | null>(null);
const saving = ref(false);

// Delete states
const readToDelete = ref<Read | null>(null);
const deleting = ref(false);

// View states
const selectedRead = ref<Read | null>(null);

// Snackbar
const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
});

// ============================================
// TABLE HEADERS
// ============================================

const headers = [
  { title: 'Nombre', key: 'name', sortable: true },
  { title: 'Usuario', key: 'user_id', sortable: true },
  { title: 'Sensor', key: 'sensor', sortable: false },
  { title: 'Bomba', key: 'pump', sortable: false },
  { title: 'Ventilador', key: 'fan', sortable: false },
  { title: 'Humo', key: 'smoke', sortable: false },
  { title: 'Timestamp', key: 'timestamp', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'center' as const },
];

// ============================================
// VALIDATION RULES
// ============================================

const rules = {
  required: (v: any) => (v !== null && v !== undefined && v !== '') || 'Este campo es requerido',
  minLength: (min: number) => (v: string) => 
    (v && v.length >= min) || `Mínimo ${min} caracteres`,
  humidity: (v: number) => {
    if (v === null || v === undefined) return 'Este campo es requerido';
    return (v >= 0 && v <= 100) || 'Debe estar entre 0 y 100';
  },
};

// ============================================
// COMPUTED
// ============================================

const filteredReads = computed(() => {
  if (!search.value) return reads.value;
  
  const searchLower = search.value.toLowerCase();
  return reads.value.filter((read) => {
    return (
      read.name.toLowerCase().includes(searchLower) ||
      read.id.toString().includes(searchLower)
    );
  });
});

// ============================================
// METHODS
// ============================================

const loadReads = async () => {
  loading.value = true;
  try {
    reads.value = await api.get<Read[]>('/reads');
  } catch (error) {
    showSnackbar('Error al cargar lecturas', 'error');
    console.error('Error loading reads:', error);
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  isEditing.value = false;
  editingReadId.value = null;
  formData.value = {
    name: '',
    user_id: null,
    includeSensor: false,
    sensor: {
      humidity: 0,
      temperature: 0,
    },
    includePump: false,
    pump: {
      status: false,
    },
    includeFan: false,
    fan: {
      status: false,
    },
    includeSmoke: false,
    smoke: {
      status: false,
    },
  };
  errors.value = {
    name: '',
    user_id: '',
    sensor: { humidity: '', temperature: '' },
    pump: {},
    fan: {},
    smoke: {},
  };
  formError.value = '';
  dialog.value = true;
};

const editRead = (read: Read) => {
  isEditing.value = true;
  editingReadId.value = read.id;
  formData.value = {
    name: read.name,
    user_id: read.user_id || null,
    includeSensor: !!read.sensor,
    sensor: read.sensor ? {
      humidity: read.sensor.humidity,
      temperature: read.sensor.temperature,
    } : {
      humidity: 0,
      temperature: 0,
    },
    includePump: !!read.pump,
    pump: read.pump ? {
      status: read.pump.status,
    } : {
      status: false,
    },
    includeFan: !!read.fan,
    fan: read.fan ? {
      status: read.fan.status,
    } : {
      status: false,
    },
    includeSmoke: !!read.smoke,
    smoke: read.smoke ? {
      status: read.smoke.status,
    } : {
      status: false,
    },
  };
  errors.value = {
    name: '',
    user_id: '',
    sensor: { humidity: '', temperature: '' },
    pump: {},
    fan: {},
    smoke: {},
  };
  formError.value = '';
  viewDialog.value = false;
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  formRef.value?.reset();
};

const saveRead = async () => {
  if (!formValid.value) return;

  saving.value = true;
  errors.value = {
    name: '',
    user_id: '',
    sensor: { humidity: '', temperature: '' },
    pump: {},
    fan: {},
    smoke: {},
  };
  formError.value = '';

  try {
    const readData: any = {
      name: formData.value.name,
      user_id: formData.value.user_id || undefined,
    };

    if (formData.value.includeSensor) {
      readData.sensor = {
        humidity: formData.value.sensor.humidity,
        temperature: formData.value.sensor.temperature,
      };
    }

    if (formData.value.includePump) {
      readData.pump = {
        status: formData.value.pump.status,
      };
    }

    if (formData.value.includeFan) {
      readData.fan = {
        status: formData.value.fan.status,
      };
    }

    if (formData.value.includeSmoke) {
      readData.smoke = {
        status: formData.value.smoke.status,
      };
    }

    if (isEditing.value && editingReadId.value) {
      // Para edición, solo actualizamos campos principales
      const updateData: any = {
        name: formData.value.name,
        user_id: formData.value.user_id || undefined,
      };
      await api.put<Read>(`/reads/${editingReadId.value}`, updateData);
      showSnackbar('Lectura actualizada correctamente', 'success');
    } else {
      await api.post<Read>('/reads', readData);
      showSnackbar('Lectura creada correctamente', 'success');
    }

    closeDialog();
    await loadReads();
  } catch (error: any) {
    const errorMessage = error.message || 'Error al guardar lectura';
    formError.value = errorMessage;
    showSnackbar(errorMessage, 'error');
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (read: Read) => {
  readToDelete.value = read;
  deleteDialog.value = true;
};

const deleteReadConfirmed = async () => {
  if (!readToDelete.value) return;

  deleting.value = true;
  try {
    await api.delete(`/reads/${readToDelete.value.id}`);
    showSnackbar('Lectura eliminada correctamente', 'success');
    deleteDialog.value = false;
    await loadReads();
  } catch (error) {
    showSnackbar('Error al eliminar lectura', 'error');
    console.error('Error deleting read:', error);
  } finally {
    deleting.value = false;
  }
};

const viewRead = (read: Read) => {
  selectedRead.value = read;
  viewDialog.value = true;
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
    second: '2-digit',
  }).format(date);
};

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadReads();
});
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}
</style>
