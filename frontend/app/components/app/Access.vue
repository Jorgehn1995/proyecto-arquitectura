<template>
  <v-container fluid>
    <!-- Header con título y botón para agregar -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <div>
            <h1 class="text-h4 font-weight-bold">Registro de Accesos</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Administra los registros de acceso al sistema</p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateDialog"
          >
            Nuevo Acceso
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
          label="Buscar accesos..."
          density="comfortable"
          clearable
          hide-details
        />
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center justify-end">
        <v-chip
          class="mr-2"
          prepend-icon="mdi-login"
          color="primary"
          variant="tonal"
        >
          Total: {{ accesses.length }}
        </v-chip>
        <v-btn
          icon="mdi-refresh"
          variant="text"
          @click="loadAccesses"
          :loading="loading"
        />
      </v-col>
    </v-row>

    <!-- Tabla de accesos -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredAccesses"
        :loading="loading"
        :search="search"
        item-value="id"
        class="elevation-0"
        :items-per-page="15"
      >
        <!-- Loading -->
        <template #loading>
          <v-skeleton-loader type="table-row@5" />
        </template>

        <!-- Column: ID -->
        <template #item.id="{ item }">
          <div class="d-flex align-center py-2">
            <v-icon class="mr-3" color="primary">mdi-key</v-icon>
            <div>
              <div class="font-weight-medium">#{{ item.id }}</div>
              <div class="text-caption text-medium-emphasis">Registro</div>
            </div>
          </div>
        </template>

        <!-- Column: Usuario -->
        <template #item.user_id="{ item }">
          <div class="d-flex align-center">
            <v-avatar
              :color="getAvatarColor(item.user_id)"
              size="32"
              class="mr-2"
            >
              <span class="text-caption text-white">
                {{ getUserInitials(item.user_id) }}
              </span>
            </v-avatar>
            <div>
              <v-chip
                size="small"
                color="info"
                variant="tonal"
                prepend-icon="mdi-account"
              >
                Usuario #{{ item.user_id }}
              </v-chip>
              <div v-if="getUserName(item.user_id)" class="text-caption text-medium-emphasis mt-1">
                {{ getUserName(item.user_id) }}
              </div>
            </div>
          </div>
        </template>

        <!-- Column: Timestamp -->
        <template #item.timestamp="{ item }">
          <div class="d-flex align-center">
            <v-icon size="small" class="mr-2" color="grey">mdi-clock-outline</v-icon>
            <div>
              <div class="text-caption font-weight-medium">
                {{ formatTime(item.timestamp) }}
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ formatDate(item.timestamp) }}
              </div>
            </div>
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
                  @click="viewAccess(item)"
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
            <v-icon size="64" color="grey-lighten-1">mdi-login-variant</v-icon>
            <p class="text-h6 text-medium-emphasis mt-4">No hay registros de acceso</p>
            <v-btn color="primary" class="mt-2" @click="openCreateDialog">
              Registrar primer acceso
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Dialog para Crear Acceso -->
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5 text-white">Nuevo Registro de Acceso</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model.number="formData.user_id"
                  label="ID de Usuario *"
                  prepend-inner-icon="mdi-account"
                  type="number"
                  :rules="[rules.required, rules.positiveNumber]"
                  :error-messages="errors.user_id"
                  hint="Ingrese el ID del usuario que accede"
                  persistent-hint
                />
              </v-col>

              <!-- Información del usuario si existe -->
              <v-col v-if="selectedUserPreview" cols="12">
                <v-card variant="outlined" color="success">
                  <v-card-text>
                    <div class="d-flex align-center">
                      <v-avatar
                        :color="getAvatarColor(selectedUserPreview.id)"
                        size="40"
                        class="mr-3"
                      >
                        <span class="text-h6 text-white">
                          {{ getInitials(selectedUserPreview.first_name, selectedUserPreview.last_name) }}
                        </span>
                      </v-avatar>
                      <div>
                        <div class="font-weight-medium">
                          {{ selectedUserPreview.first_name }} {{ selectedUserPreview.last_name }}
                        </div>
                        <div class="text-caption">{{ selectedUserPreview.email }}</div>
                        <div v-if="selectedUserPreview.rfid_tag" class="text-caption">
                          <v-icon size="x-small" class="mr-1">mdi-card-account-details</v-icon>
                          {{ selectedUserPreview.rfid_tag }}
                        </div>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
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
            @click="saveAccess"
            :loading="saving"
            :disabled="!formValid"
          >
            Registrar Acceso
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
            Esta acción no se puede deshacer
          </v-alert>
          
          <p class="text-body-1">
            ¿Está seguro que desea eliminar el registro de acceso 
            <strong>#{{ accessToDelete?.id }}</strong>?
          </p>
          
          <div v-if="accessToDelete" class="mt-4 pa-3 rounded">
            <div class="d-flex align-center mb-2">
              <v-icon size="small" class="mr-2">mdi-account</v-icon>
              <span class="text-caption">Usuario #{{ accessToDelete.user_id }}</span>
            </div>
            <div class="d-flex align-center">
              <v-icon size="small" class="mr-2">mdi-calendar-clock</v-icon>
              <span class="text-caption">{{ formatDateTime(accessToDelete.timestamp) }}</span>
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
            @click="deleteAccessConfirmed"
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de Detalles del Acceso -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card v-if="selectedAccess">
        <v-card-title>
          <span class="text-h5 text-white">Detalles del Acceso</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <div class="text-center mb-6">
            <v-icon size="64" color="primary">mdi-login</v-icon>
            <h2 class="text-h5 mt-3">Registro #{{ selectedAccess.id }}</h2>
            <p class="text-caption text-medium-emphasis">Acceso al Sistema</p>
          </div>

          <v-list>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-identifier</v-icon>
              </template>
              <v-list-item-title>ID del Registro</v-list-item-title>
              <v-list-item-subtitle>#{{ selectedAccess.id }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-account</v-icon>
              </template>
              <v-list-item-title>Usuario</v-list-item-title>
              <v-list-item-subtitle>
                <div class="d-flex align-center mt-1">
                  <v-chip size="small" color="info" variant="tonal">
                    Usuario #{{ selectedAccess.user_id }}
                  </v-chip>
                  <span v-if="getUserName(selectedAccess.user_id)" class="ml-2 text-caption">
                    {{ getUserName(selectedAccess.user_id) }}
                  </span>
                </div>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-calendar-clock</v-icon>
              </template>
              <v-list-item-title>Fecha y Hora</v-list-item-title>
              <v-list-item-subtitle>
                {{ formatDateTime(selectedAccess.timestamp) }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-clock-outline</v-icon>
              </template>
              <v-list-item-title>Hora</v-list-item-title>
              <v-list-item-subtitle>{{ formatTime(selectedAccess.timestamp) }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-calendar</v-icon>
              </template>
              <v-list-item-title>Fecha</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(selectedAccess.timestamp) }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions class="px-6 pb-6">
          <v-spacer />
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
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '~/composables/base/useApi';
import type { User } from '~/types/app';

const api = useApi();

// ============================================
// INTERFACES
// ============================================

interface Access {
  id: number;
  user_id: number;
  timestamp: string;
}

// ============================================
// STATE
// ============================================

const accesses = ref<Access[]>([]);
const users = ref<User[]>([]);
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
  user_id: null as number | null,
});
const errors = ref({
  user_id: '',
});
const formError = ref('');
const saving = ref(false);

// Delete states
const accessToDelete = ref<Access | null>(null);
const deleting = ref(false);

// View states
const selectedAccess = ref<Access | null>(null);
const selectedUserPreview = ref<User | null>(null);

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
  { title: 'ID', key: 'id', sortable: true },
  { title: 'Usuario', key: 'user_id', sortable: true },
  { title: 'Fecha y Hora', key: 'timestamp', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'center' as const },
];

// ============================================
// VALIDATION RULES
// ============================================

const rules = {
  required: (v: any) => (v !== null && v !== undefined && v !== '') || 'Este campo es requerido',
  positiveNumber: (v: number) => {
    if (v === null || v === undefined) return 'Este campo es requerido';
    return v > 0 || 'Debe ser un número positivo';
  },
};

// ============================================
// COMPUTED
// ============================================

const filteredAccesses = computed(() => {
  if (!search.value) return accesses.value;
  
  const searchLower = search.value.toLowerCase();
  return accesses.value.filter((access) => {
    const userName = getUserName(access.user_id);
    return (
      access.id.toString().includes(searchLower) ||
      access.user_id.toString().includes(searchLower) ||
      (userName && userName.toLowerCase().includes(searchLower)) ||
      formatDateTime(access.timestamp).toLowerCase().includes(searchLower)
    );
  });
});

// ============================================
// WATCHERS
// ============================================

watch(() => formData.value.user_id, async (newUserId) => {
  if (newUserId && newUserId > 0) {
    await loadUserPreview(newUserId);
  } else {
    selectedUserPreview.value = null;
  }
});

// ============================================
// METHODS
// ============================================

const loadAccesses = async () => {
  loading.value = true;
  try {
    accesses.value = await api.get<Access[]>('/access');
  } catch (error) {
    showSnackbar('Error al cargar accesos', 'error');
    console.error('Error loading accesses:', error);
  } finally {
    loading.value = false;
  }
};

const loadUsers = async () => {
  try {
    users.value = await api.get<User[]>('/users');
  } catch (error) {
    console.error('Error loading users:', error);
  }
};

const loadUserPreview = async (userId: number) => {
  try {
    selectedUserPreview.value = await api.get<User>(`/users/${userId}`);
    formError.value = '';
  } catch (error) {
    selectedUserPreview.value = null;
    formError.value = 'Usuario no encontrado';
  }
};

const openCreateDialog = () => {
  formData.value = {
    user_id: null,
  };
  errors.value = {
    user_id: '',
  };
  formError.value = '';
  selectedUserPreview.value = null;
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  formRef.value?.reset();
  selectedUserPreview.value = null;
};

const saveAccess = async () => {
  if (!formValid.value) return;

  saving.value = true;
  errors.value = {
    user_id: '',
  };
  formError.value = '';

  try {
    const accessData = {
      user_id: formData.value.user_id!,
    };

    await api.post<Access>('/access', accessData);
    showSnackbar('Acceso registrado correctamente', 'success');

    closeDialog();
    await loadAccesses();
  } catch (error: any) {
    const errorMessage = error.message || 'Error al registrar acceso';
    formError.value = errorMessage;
    
    if (errorMessage.toLowerCase().includes('user') || errorMessage.toLowerCase().includes('usuario')) {
      errors.value.user_id = errorMessage;
    }
    
    showSnackbar(errorMessage, 'error');
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (access: Access) => {
  accessToDelete.value = access;
  deleteDialog.value = true;
};

const deleteAccessConfirmed = async () => {
  if (!accessToDelete.value) return;

  deleting.value = true;
  try {
    await api.delete(`/access/${accessToDelete.value.id}`);
    showSnackbar('Acceso eliminado correctamente', 'success');
    deleteDialog.value = false;
    await loadAccesses();
  } catch (error) {
    showSnackbar('Error al eliminar acceso', 'error');
    console.error('Error deleting access:', error);
  } finally {
    deleting.value = false;
  }
};

const viewAccess = (access: Access) => {
  selectedAccess.value = access;
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

const getUserName = (userId: number): string | null => {
  const user = users.value.find(u => u.id === userId);
  return user ? `${user.first_name} ${user.last_name}` : null;
};

const getInitials = (firstName: string, lastName: string): string => {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
};

const getUserInitials = (userId: number): string => {
  const user = users.value.find(u => u.id === userId);
  if (user) {
    return getInitials(user.first_name, user.last_name);
  }
  return 'U';
};

const getAvatarColor = (identifier: number): string => {
  const colors = [
    'primary',
    'secondary',
    'success',
    'info',
    'warning',
    'error',
    'purple',
    'indigo',
    'pink',
    'teal',
  ];
  const index = identifier % colors.length;
  return colors[index] || 'primary';
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
};

const formatTime = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date);
};

const formatDateTime = (dateString: string): string => {
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

onMounted(async () => {
  await loadUsers();
  await loadAccesses();
});
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}
</style>
