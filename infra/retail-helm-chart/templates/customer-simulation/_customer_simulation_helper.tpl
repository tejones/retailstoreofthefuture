{{/*
Expand the name of the chart.
*/}}
{{- define "customerSimulation.name" -}}
{{- .Values.customerSimulationService.nameOverride | default "customer-simulation" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "customerSimulation.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "customerSimulation.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "customerSimulation.selectorLabels" -}}
app.kubernetes.io/name: {{ include "customerSimulation.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "customerSimulation.serviceAccountName" -}}
{{- if .Values.customerSimulationService.serviceAccount.create }}
{{- .Values.customerSimulationService.serviceAccount.name | default (include "customerSimulation.name" .) }}-serviceaccount
{{- else }}
{{- .Values.customerSimulationService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "customerSimulation.serviceName" -}}
{{- include "customerSimulation.name" . }}-svc
{{- end }}

{{- define "customerSimulation.servicePort" -}}
{{- .Values.customerSimulationService.servicePort | default 80 -}}
{{- end }}
