# -*- coding: utf-8 -*-
from django.db import models

SEXO_CHOICES = (
    ('F', 'Femenino'),
    ('M', 'Masculino'),
)

class cat_institucion(models.Model):
    nombre_comercial    = models.CharField(max_length=60)
    razon_social        = models.CharField(max_length=60)
    RUC                 = models.CharField(unique=True, max_length=60)
    direccion           = models.CharField(max_length=60)
    descripcion         = models.CharField(max_length=200)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('instituciones')
    def __unicode__(self):
        return "% | %" % self.nombre_comercial, self.RUC

class cat_fondo(models.Model):
    nombre              = models.CharField(max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta:
       verbose_name_plural = _('fondos')
    def __unicode__(self):
       return self.nombre

class cat_departamento(models.Model):
    nombre              = models.CharField(unique=True, max_length=60)
    class Meta:
        verbose_name_plural = _('departamentos')
    def __unicode__(self):      
        return self.nombre

class cat_municipio(models.Model):
    departamento        = models.ForeignKey(cat_departamento)
    num_municipio       = models.IntegerField()
    nombre              = models.CharField(unique=True, max_length=60)
    class Meta:
        verbose_name_plural = _('municipios')
    def __unicode__(self):
        return "%s | %s" % self.departamento.nombre, self.nombre

class cat_banco(models.Model):
    institucion         = models.ForeignKey(cat_institucion)
    nombre              = models.CharField(max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('bancos')
    def __unicode__(self):
        return "%s | %s" % self.institucion, self.nombre

class cat_moneda(models.Model):
    nombre              = models.CharField(max_length=60)
    simbolo             = models.CharField(max_length=60)
    alias               = models.CharField(max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('oficinas')
    def __unicode__(self):
        return "%s | %s" % self.nombre, self.simbolo

class cat_oficina(models.Model):
    institucion         = models.ForeignKey(cat_institucion)
    nombre              = models.CharField(max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('oficinas')
    def __unicode__(self):
        return "%s | %s" % self.institucion, self.nombre

class cat_gerencia(models.Model):
    institucion         = models.ForeignKey(cat_institucion)
    nombre              = models.CharField(max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('gerencias')
    def __unicode__(self):
        return "%s | %s" % self.institucion, self.nombre

class cat_cargo(models.Model):
    institucion         = models.ForeignKey(cat_institucion)
    gerencia            = models.ForeignKey(cat_gerencia)   
    nombre              = models.CharField(unique=True, max_length=60)
    estado              = models.BooleanField(default=True)
    class Meta: 
        verbose_name_plural = _('cargos')
    def __unicode__(self):
        return "%s | %s | %s" % self.institucion, self.gerencia, self.nombre

class cat_gentilicio(models.Model):
    nombre              = models.CharField(unique=True, max_length=60)
    abreviacion         = models.CharField(unique=True, max_length=60)

    class Meta:
        verbose_name_plural = _('estado civil')
    def __unicode__(self):
        return self.gentilicio

class cat_estado_civil(models.Model):
    nombre              = models.CharField(max_length=60)
    class Meta:     
        verbose_name_plural = _('estado civil')
    def __unicode__(self):
        return self.nombre

class cat_estado_empleado(models.Model):
    nombre              = models.models.CharField(max_length=60)
    class Meta:     
        verbose_name_plural = _('estado empleado')
    def __unicode__(self):
        return self.nombre
    
class info_empleado(models.Model):
    institucion         = models.ForeignKey(cat_institucion)
    codigo              = models.CharField(max_length=60)
    gentilicio          = models.ForeignKey(cat_gentilicio) #pendiente
    nombres             = models.CharField(max_length=60)
    apellidos           = models.CharField(max_length=60)
    fecha_nacimiento    = models.DateField()    
    identificacion      = models.CharField(unique=True, max_length=60)  
    seguro_social       = models.CharField(unique=True, max_length=60)  
    departamento        = models.ForeignKey(cat_departamento)
    municipio           = models.ForeignKey(cat_municipio)
    direccion           = models.CharField(max_length=60)
    telefono            = models.PositiveIntegerField()
    estado_civil        = models.ForeignKey(cat_estado_civil) 
    estado_empleado     = models.ForeignKey(cat_estado_empleado)
    foto                = models.ImageField(upload_to='fotos')
    class Meta:
        verbose_name_plural = _('información personal')
    def __unicode__(self):
        return "%s %s" % self.nombres, self.apellidos

class info_identificacion(models.Model):
    nombre              = models.CharField(max_length=60)
    numero              = models.CharField(max_length=60)
    mascara             = models.CharField(max_length=60)
    empleado            = models.ForeignKey(info_empleado)
    estado              = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = _('info_identificacions')
    def __unicode__(self):
        return "%s %s | %s | %s" % self.empleado.nombres, self.empleado.apellidos, self.nombre, self.numero

class info_laboral(models.Model):
    empleado            = models.FloatField(info_empleado)
    oficina             = models.ForeignKey(cat_oficina)    
    cargo               = models.ForeignKey(cat_cargo)  
    fecha_ingreso       = models.DateField()
    fecha_retiro        = models.DateField()
    salario             = models.DecimalField(max_digits=19, decimal_places=2)
    moneda              = models.ForeignKey(cat_moneda)
    banco               = models.ForeignKey(cat_banco)
    cuenta_bancaria     = models.PositiveIntegerField()
    control_horario     = models.BooleanField(default=True)
    pago_extras         = models.BooleanField()
    pago_incentivos     = models.BooleanField()
    pago_depreciacion   = models.BooleanField()
    vacaciones_acum     = models.DecimalField(max_digits=19, decimal_places=2)
    class Meta:
        verbose_name_plural = _('información laboral')
    def __unicode__(self):
        return "%s %s | %s | %s" % self.nombres, self.apellidos, self.salario, self.moneda

class param_IR(models.Model):
    renta_de            = models.DecimalField(max_digits=19, decimal_places=2)
    renta_hasta         = models.DecimalField(max_digits=19, decimal_places=2)
    impuesto_base       = models.DecimalField(max_digits=19, decimal_places=2)
    tasa                = models.DecimalField(max_digits=19, decimal_places=2)
    sobre_exceso        = models.DecimalField(max_digits=19, decimal_places=2)
    moneda              = models.ForeignKey(cat_moneda)
    class Meta:
        verbose_name_plural = _('param_IRs')
    def __unicode__(self):
        pass