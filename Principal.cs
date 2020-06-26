using System;

namespace CIV_CommonValidators
{
    public class LayoutValidators
    {
        private String AjustarNumeroCaracteres(String baseString, int numCaracters)
        {
            if (baseString.Length > numCaracters)
            {
                return $"A informação enviada ultrapassa {numCaracters} dígitos";
            }
            else
            {
                while (baseString.Length < numCaracters)
                {
                    baseString = '0' + baseString;
                }
                return baseString;
            }
        }
        public String AjustarNumeroContratoVeiculos(String numContrato)
        {
            return AjustarNumeroCaracteres(numContrato, 8);
        }

        public String AjustarCPF(String numCpf)
        {
            return AjustarNumeroCaracteres(numCpf, 11);
        }

        public String CapitalizarString(String baseString)
        {
            return baseString.ToUpper();
        }

    }
}
