<template>
  <v-container fluid>
    <!-- Header con título y botón para agregar -->
    <v-row class="mb-4">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <div>
            <h1 class="text-h4 font-weight-bold">Gestión de Usuarios</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Administra los usuarios del sistema</p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateDialog"
          >
            Nuevo Usuario
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
          label="Buscar usuarios..."
          
          density="comfortable"
          clearable
          hide-details
        />
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center justify-end">
        <v-chip
          class="mr-2"
          prepend-icon="mdi-account-group"
          color="primary"
          variant="tonal"
        >
          Total: {{ users.length }}
        </v-chip>
        <v-btn
          icon="mdi-refresh"
          variant="text"
          @click="loadUsers"
          :loading="loading"
        />
      </v-col>
    </v-row>

    <!-- Tabla de usuarios -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        :search="search"
        item-value="id"
        class="elevation-0"
      >
        <!-- Loading -->
        <template #loading>
          <v-skeleton-loader type="table-row@5" />
        </template>

        <!-- Column: Avatar y Nombre -->
        <template #item.first_name="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar
              :color="getAvatarColor(item.first_name)"
              size="40"
              class="mr-3"
            >
              <span class="text-h6 text-white">
                {{ getInitials(item.first_name, item.last_name) }}
              </span>
            </v-avatar>
            <div>
              <div class="font-weight-medium">
                {{ item.first_name }} {{ item.last_name }}
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ item.email }}
              </div>
            </div>
          </div>
        </template>

        <!-- Column: RFID Tag -->
        <template #item.rfid_tag="{ item }">
          <v-chip
            v-if="item.rfid_tag"
            size="small"
            color="success"
            variant="tonal"
            prepend-icon="mdi-card-account-details"
          >
            {{ item.rfid_tag }}
          </v-chip>
          <span v-else class="text-medium-emphasis text-caption">Sin tag</span>
        </template>

        <!-- Column: Fecha de Creación -->
        <template #item.created_at="{ item }">
          <div class="text-caption">
            {{ formatDate(item.created_at) }}
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
                  @click="viewUser(item)"
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
                  @click="editUser(item)"
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
            <v-icon size="64" color="grey-lighten-1">mdi-account-off</v-icon>
            <p class="text-h6 text-medium-emphasis mt-4">No hay usuarios registrados</p>
            <v-btn color="primary" class="mt-2" @click="openCreateDialog">
              Crear primer usuario
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Dialog para Crear/Editar Usuario -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title >
          <span class="text-h5 text-white">
            {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.first_name"
                  label="Nombre *"
                  prepend-inner-icon="mdi-account"
                  
                  :rules="[rules.required, rules.minLength(2)]"
                  :error-messages="errors.first_name"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.last_name"
                  label="Apellido *"
                  prepend-inner-icon="mdi-account"
                  
                  :rules="[rules.required, rules.minLength(2)]"
                  :error-messages="errors.last_name"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.email"
                  label="Email *"
                  prepend-inner-icon="mdi-email"
                  
                  type="email"
                  :rules="[rules.required, rules.email]"
                  :error-messages="errors.email"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.rfid_tag"
                  label="Tag RFID (opcional)"
                  prepend-inner-icon="mdi-card-account-details"
                  
                  hint="Tag único para identificación RFID"
                  persistent-hint
                  :error-messages="errors.rfid_tag"
                />
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
            @click="saveUser"
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
        <v-card-title >
          <span class="text-h5 text-white">Confirmar Eliminación</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-alert type="warning" variant="tonal" class="mb-4">
            Esta acción no se puede deshacer
          </v-alert>
          
          <p class="text-body-1">
            ¿Está seguro que desea eliminar al usuario 
            <strong>{{ userToDelete?.first_name }} {{ userToDelete?.last_name }}</strong>?
          </p>
          
          <div v-if="userToDelete" class="mt-4 pa-3 rounded">
            <div class="d-flex align-center mb-2">
              <v-icon size="small" class="mr-2">mdi-email</v-icon>
              <span class="text-caption">{{ userToDelete.email }}</span>
            </div>
            <div v-if="userToDelete.rfid_tag" class="d-flex align-center">
              <v-icon size="small" class="mr-2">mdi-card-account-details</v-icon>
              <span class="text-caption">{{ userToDelete.rfid_tag }}</span>
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
            @click="deleteUserConfirmed"
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de Detalles del Usuario -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card v-if="selectedUser">
        <v-card-title >
          <span class="text-h5 text-white">Detalles del Usuario</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <div class="text-center mb-6">
            <v-avatar
              :color="getAvatarColor(selectedUser.first_name)"
              size="80"
            >
              <span class="text-h3 text-white">
                {{ getInitials(selectedUser.first_name, selectedUser.last_name) }}
              </span>
            </v-avatar>
            <h2 class="text-h5 mt-3">
              {{ selectedUser.first_name }} {{ selectedUser.last_name }}
            </h2>
          </div>

          <v-list>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-email</v-icon>
              </template>
              <v-list-item-title>Email</v-list-item-title>
              <v-list-item-subtitle>{{ selectedUser.email }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-card-account-details</v-icon>
              </template>
              <v-list-item-title>Tag RFID</v-list-item-title>
              <v-list-item-subtitle>
                {{ selectedUser.rfid_tag || 'No asignado' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-calendar</v-icon>
              </template>
              <v-list-item-title>Fecha de Creación</v-list-item-title>
              <v-list-item-subtitle>
                {{ formatDate(selectedUser.created_at) }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-identifier</v-icon>
              </template>
              <v-list-item-title>ID</v-list-item-title>
              <v-list-item-subtitle>#{{ selectedUser.id }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions class="px-6 pb-6">
          <v-spacer />
          <v-btn
            color="primary"
            variant="text"
            @click="editUser(selectedUser)"
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
import type { User } from '~/types/app';

const api = useApi();

// ============================================
// STATE
// ============================================

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
  first_name: '',
  last_name: '',
  email: '',
  rfid_tag: '',
});
const errors = ref({
  first_name: '',
  last_name: '',
  email: '',
  rfid_tag: '',
});
const formError = ref('');
const isEditing = ref(false);
const editingUserId = ref<number | null>(null);
const saving = ref(false);

// Delete states
const userToDelete = ref<User | null>(null);
const deleting = ref(false);

// View states
const selectedUser = ref<User | null>(null);

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
  { title: 'Usuario', key: 'first_name', sortable: true },
  { title: 'Tag RFID', key: 'rfid_tag', sortable: true },
  { title: 'Fecha de Creación', key: 'created_at', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'center' as const },
];

// ============================================
// VALIDATION RULES
// ============================================

const rules = {
  required: (v: string) => !!v || 'Este campo es requerido',
  minLength: (min: number) => (v: string) => 
    (v && v.length >= min) || `Mínimo ${min} caracteres`,
  email: (v: string) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(v) || 'Email inválido';
  },
};

// ============================================
// COMPUTED
// ============================================

const filteredUsers = computed(() => {
  if (!search.value) return users.value;
  
  const searchLower = search.value.toLowerCase();
  return users.value.filter((user) => {
    return (
      user.first_name.toLowerCase().includes(searchLower) ||
      user.last_name.toLowerCase().includes(searchLower) ||
      user.email.toLowerCase().includes(searchLower) ||
      (user.rfid_tag && user.rfid_tag.toLowerCase().includes(searchLower))
    );
  });
});

// ============================================
// METHODS
// ============================================

const loadUsers = async () => {
  loading.value = true;
  try {
    users.value = await api.get<User[]>('/users');
  } catch (error) {
    showSnackbar('Error al cargar usuarios', 'error');
    console.error('Error loading users:', error);
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  isEditing.value = false;
  editingUserId.value = null;
  formData.value = {
    first_name: '',
    last_name: '',
    email: '',
    rfid_tag: '',
  };
  errors.value = {
    first_name: '',
    last_name: '',
    email: '',
    rfid_tag: '',
  };
  formError.value = '';
  dialog.value = true;
};

const editUser = (user: User) => {
  isEditing.value = true;
  editingUserId.value = user.id;
  formData.value = {
    first_name: user.first_name,
    last_name: user.last_name,
    email: user.email,
    rfid_tag: user.rfid_tag || '',
  };
  errors.value = {
    first_name: '',
    last_name: '',
    email: '',
    rfid_tag: '',
  };
  formError.value = '';
  viewDialog.value = false;
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  formRef.value?.reset();
};

const saveUser = async () => {
  if (!formValid.value) return;

  saving.value = true;
  errors.value = {
    first_name: '',
    last_name: '',
    email: '',
    rfid_tag: '',
  };
  formError.value = '';

  try {
    const userData = {
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      email: formData.value.email,
      rfid_tag: formData.value.rfid_tag || undefined,
    };

    if (isEditing.value && editingUserId.value) {
      await api.put<User>(`/users/${editingUserId.value}`, userData);
      showSnackbar('Usuario actualizado correctamente', 'success');
    } else {
      await api.post<User>('/users', userData);
      showSnackbar('Usuario creado correctamente', 'success');
    }

    closeDialog();
    await loadUsers();
  } catch (error: any) {
    const errorMessage = error.message || 'Error al guardar usuario';
    formError.value = errorMessage;
    
    // Parse specific field errors if available
    if (errorMessage.includes('Email')) {
      errors.value.email = errorMessage;
    } else if (errorMessage.includes('RFID') || errorMessage.includes('tag')) {
      errors.value.rfid_tag = errorMessage;
    }
    
    showSnackbar(errorMessage, 'error');
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (user: User) => {
  userToDelete.value = user;
  deleteDialog.value = true;
};

const deleteUserConfirmed = async () => {
  if (!userToDelete.value) return;

  deleting.value = true;
  try {
    await api.delete(`/users/${userToDelete.value.id}`);
    showSnackbar('Usuario eliminado correctamente', 'success');
    deleteDialog.value = false;
    await loadUsers();
  } catch (error) {
    showSnackbar('Error al eliminar usuario', 'error');
    console.error('Error deleting user:', error);
  } finally {
    deleting.value = false;
  }
};

const viewUser = (user: User) => {
  selectedUser.value = user;
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

const getInitials = (firstName: string, lastName: string): string => {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
};

const getAvatarColor = (name: string): string => {
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
  const index = name.charCodeAt(0) % colors.length;
  return colors[index] || 'primary';
};

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
  loadUsers();
});
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}
</style>
