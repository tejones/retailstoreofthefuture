{{/*
Expand the name of the chart.
*/}}
{{- define "fepump.name" -}}
{{- .Values.fepumpService.nameOverride | default "fepump" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fepump.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "fepump.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fepump.selectorLabels" -}}
app.kubernetes.io/name: {{ include "fepump.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "fepump.serviceAccountName" -}}
{{- if .Values.fepumpService.serviceAccount.create }}
{{- .Values.fepumpService.serviceAccount.name | default (include "fepump.name" .) }}-serviceaccount
{{- else }}
{{- .Values.fepumpService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "fepump.serviceName" -}}
{{- include "fepump.name" . }}-svc
{{- end }}

{{- define "fepump.servicePort" -}}
{{- .Values.fepumpService.servicePort | default 80 -}}
{{- end }}
