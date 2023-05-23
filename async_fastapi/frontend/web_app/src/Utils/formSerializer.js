export default function serializeForm(formNode) {
    const { elements } = formNode;

    const data = new FormData();

    Array.from(elements)
        .filter((item) => !!item.name)
        .forEach((element) => {
            if (element.checkValidity()) {
                const { name, type } = element;
                const value = type === 'checkbox' ? element.checked : element.value;
                data.append(name, value);
            }
        })

    return Object.fromEntries(data.entries())
}