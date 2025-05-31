from django.contrib import admin
from .models import Student, Attendance, AttendanceUser, StudentAttendanceRecord


class AttendanceUserAdmin(admin.ModelAdmin):
    """Admin configuration for AttendanceUser model"""

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('password_hash', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
        ('Security', {'fields': ('password_hash',)}),
    )


class StudentAttendanceRecordAdmin(admin.ModelAdmin):
    """Admin configuration for StudentAttendanceRecord model"""

    list_display = (
        'student_name', 'student_roll_number', 'student_class',
        'attendance_status', 'attendance_date', 'attendance_time',
        'session_type', 'subject_name', 'marked_by'
    )
    list_filter = (
        'attendance_status', 'attendance_date', 'session_type',
        'student_class', 'subject_name', 'marked_by'
    )
    search_fields = (
        'student_name', 'student_roll_number', 'student_email',
        'subject_name', 'subject_code', 'marked_by'
    )
    ordering = ('-attendance_date', '-attendance_time')
    readonly_fields = ('created_at', 'updated_at', 'attendance_datetime')

    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'student_roll_number', 'student_class', 'student_email')
        }),
        ('Attendance Details', {
            'fields': ('attendance_status', 'attendance_date', 'attendance_time', 'attendance_datetime')
        }),
        ('Session Information', {
            'fields': ('session_type', 'subject_name', 'subject_code', 'location')
        }),
        ('Additional Information', {
            'fields': ('marked_by', 'remarks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Add date hierarchy for easy navigation
    date_hierarchy = 'attendance_date'

    # Add actions for bulk operations
    actions = ['mark_as_present', 'mark_as_absent']

    def mark_as_present(self, request, queryset):
        queryset.update(attendance_status='Present')
        self.message_user(request, f"{queryset.count()} records marked as Present.")
    mark_as_present.short_description = "Mark selected records as Present"

    def mark_as_absent(self, request, queryset):
        queryset.update(attendance_status='Absent')
        self.message_user(request, f"{queryset.count()} records marked as Absent.")
    mark_as_absent.short_description = "Mark selected records as Absent"


admin.site.register(AttendanceUser, AttendanceUserAdmin)
admin.site.register(StudentAttendanceRecord, StudentAttendanceRecordAdmin)
admin.site.register(Student)
admin.site.register(Attendance)
