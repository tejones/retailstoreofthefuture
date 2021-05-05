{{/*
Expand the name of the chart.
*/}}
{{- define "postgres.name" -}}
{{- .Values.postgres.nameOverride| default "postgres" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "postgres.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "postgres.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "postgres.selectorLabels" -}}
app.kubernetes.io/name: {{ include "postgres.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "postgres.serviceAccountName" -}}
{{- if .Values.postgres.serviceAccount.create }}
{{- .Values.postgres.serviceAccount.name | default (include "postgres.name" .) }}-serviceaccount
{{- else }}
{{- .Values.postgres.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}



{{- define "postgres.serviceName" -}}
{{- include "postgres.name" . }}-svc
{{- end }}

{{- define "postgres.servicePort" -}}
{{- .Values.postgres.servicePort | default 5432 -}}
{{- end }}

{{- define "postgres.secretName" -}}
{{- include "postgres.name" . }}-secret
{{- end }}

{{- define "postgres.configMapName" -}}
{{- include "postgres.name" . }}-cm
{{- end }}
